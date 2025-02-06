import graphene
from django import forms as django_forms
from django.db import transaction
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_model
from core.models import Event

from ...models.product import Product
from ...models.quota import Quota
from ..product_limited import LimitedProductType


class CreateProductInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class CreateProductForm(django_forms.ModelForm):
    description = django_forms.CharField(required=False, initial="")
    quota = django_forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
        ]


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(required=True)

    product = graphene.Field(LimitedProductType)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: CreateProductInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        graphql_check_model(Product, event.scope, info, operation="create")

        form = CreateProductForm(data=input.form_data)  # type: ignore
        if not form.is_valid():
            raise ValueError(form.errors)

        product: Product = form.save(commit=False)
        product.event = event
        product.save()

        if num_available := form.cleaned_data.get("quota"):
            quota = Quota.objects.create(event=event, name=product.title)
            quota.set_quota(num_available)
            product.quotas.add(quota)

        return CreateProduct(product=product)  # type: ignore
