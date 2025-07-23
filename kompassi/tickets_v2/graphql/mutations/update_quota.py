from typing import Self

import graphene
from django import forms as django_forms
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.utils.form_utils import camel_case_keys_to_snake_case
from kompassi.event_log_v2.utils.emit import emit

from ...models.quota import Quota
from ..quota_limited import LimitedQuotaType


class QuotaForm(django_forms.ModelForm):
    quota = django_forms.IntegerField(required=True)

    class Meta:
        model = Quota
        fields = ("name",)

    @classmethod
    def from_form_data(cls, quota: Quota, form_data: dict[str, str]) -> Self:
        form_data = camel_case_keys_to_snake_case(form_data)
        return cls(form_data, instance=quota)


class UpdateQuotaInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    quota_id = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateQuota(graphene.Mutation):
    class Arguments:
        input = UpdateQuotaInput(required=True)

    quota = graphene.Field(LimitedQuotaType)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: UpdateQuotaInput,
    ):
        request: HttpRequest = info.context

        quota = Quota.objects.get(event__slug=input.event_slug, id=input.quota_id)
        form_data: dict[str, str] = input.form_data  # type: ignore

        graphql_check_instance(quota, info, operation="update")

        form = QuotaForm.from_form_data(quota, form_data)
        if not form.is_valid():
            raise django_forms.ValidationError(form.errors)  # type: ignore

        form.save()
        quota.set_quota(form.cleaned_data["quota"])

        emit(
            "tickets_v2.quota.updated",
            event=quota.event,
            quota=quota,
            request=request,
            context=quota.admin_url,
        )

        return UpdateQuota(quota=quota)  # type: ignore
