import logging
from typing import Self

import graphene
from django import forms as django_forms
from django.db import models, transaction
from django.forms.models import model_to_dict
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.models.event import Event
from core.utils.form_utils import camel_case_keys_to_snake_case
from event_log_v2.utils.emit import emit
from forms.models.field import Choice, Field, FieldType
from forms.utils.process_form_data import process_form_data

from ...models.product import Product
from ...models.quota import Quota
from ..product_limited import LimitedProductType

logger = logging.getLogger("kompassi")


class ProductForm(django_forms.ModelForm):
    description = django_forms.CharField(required=False, initial="")

    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "price",
            "max_per_order",
            "etickets_per_product",
            "available_from",
            "available_until",
        )

    @classmethod
    def from_form_data(cls, product: Product, form_data: dict[str, str]) -> Self:
        form_data = camel_case_keys_to_snake_case(form_data)
        return cls(form_data, instance=product)


class UpdateProductInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    product_id = graphene.Int(required=True)
    form_data = GenericScalar(required=True)


# Changing these fields does not trigger a new product revision to be created.
REVISION_EXEMPT_FIELDS = {"available_from", "available_until"}


# Is this a common pattern? Oughtn't it be encapsulated?
def get_quotas(event: Event, form_data: dict[str, str]) -> models.QuerySet[Quota]:
    """
    Parse a MultiSelect field with the slug `quotas` from `form_data` and
    return the corresponding Quota instances of this event.
    """
    fields = [
        Field(
            slug="quotas",
            type=FieldType.MULTI_SELECT,
            choices=[Choice(slug=str(q.id)) for q in Quota.objects.filter(event=event)],
        )
    ]

    values, warnings = process_form_data(fields, form_data)

    if warnings:
        raise ValueError(warnings)

    quota_ids: set[str] = set(values["quotas"])
    if len(quota_ids) != len(values["quotas"]):
        raise ValueError("Duplicate quota IDs")

    quotas = Quota.objects.filter(event=event, id__in=quota_ids)
    if len(quotas) != len(quota_ids):
        raise ValueError("Invalid quota IDs")

    return quotas


class UpdateProduct(graphene.Mutation):
    class Arguments:
        input = UpdateProductInput(required=True)

    product = graphene.Field(LimitedProductType)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: UpdateProductInput,
    ):
        request: HttpRequest = info.context

        product = (
            Product.objects.select_for_update(of=("self",))
            .select_related("event")
            .prefetch_related("quotas")
            .get(
                event__slug=input.event_slug,
                id=input.product_id,
                superseded_by=None,
            )
        )
        graphql_check_instance(product, info, operation="update")

        meta = product.event.tickets_v2_event_meta
        if meta is None:
            raise ValueError("Event has no tickets_v2_meta")
        event = meta.event

        form_data: dict[str, str] = input.form_data  # type: ignore

        old_values = model_to_dict(product)
        old_quota_ids = set(product.quotas.values_list("id", flat=True))

        form = ProductForm.from_form_data(product, form_data)
        if not form.is_valid():
            raise django_forms.ValidationError(form.errors)  # type: ignore

        # NOTE: product will have been mutated by the form by this point! do not trust it to contain old_values any more

        new_values = form.cleaned_data
        new_quotas = get_quotas(product.event, form_data)
        new_quota_ids = {q.id for q in new_quotas}

        changed_fields = {field_name for field_name in new_values if new_values[field_name] != old_values[field_name]}
        new_revision_fields = changed_fields - REVISION_EXEMPT_FIELDS

        if new_revision_fields:
            old_version_id = product.id

            logger.info(
                "Creating new revision of product %s due to change in %s",
                product,
                ", ".join(new_revision_fields),
            )

            product = Product(
                event=product.event,
                superseded_by=None,
                **new_values,
            )
            product.save()

            n = Product.objects.filter(event=event, id=input.product_id).update(superseded_by=product)
            n += Product.objects.filter(event=event, superseded_by=input.product_id).update(superseded_by=product)
            logger.info("Marked %d old product versions as superseded by %s", n, product)
        else:
            old_version_id = None

            logger.debug("Updating product %s in place", product)
            form.save()

        product.quotas.set(new_quotas)

        if new_quota_ids != old_quota_ids:
            logger.info(
                "Product %s quotas changed from %s to %s.",
                product,
                old_quota_ids,
                new_quota_ids,
            )

            # Update quotas of old versions
            for old_version in Product.objects.filter(
                event=event,
                superseded_by=product,
            ):
                old_version.quotas.set(new_quotas)

            meta.reticket()
        else:
            logger.debug("Product %s quotas unchanged, no need to reticket.", product)

        emit(
            "tickets_v2.product.updated",
            event=event,
            product=product,
            old_version_id=old_version_id,
            request=request,
            context=product.admin_url,
        )

        return UpdateProduct(product=product)  # type: ignore
