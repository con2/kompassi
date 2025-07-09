import graphene
from django import forms as django_forms
from django.db import transaction
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_model
from core.models import Event

from ...models.quota import Quota
from ..quota_limited import LimitedQuotaType


class CreateQuotaInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class CreateQuotaForm(django_forms.ModelForm):
    quota = django_forms.IntegerField(required=True, min_value=0)

    class Meta:
        model = Quota
        fields = ["name"]


class CreateQuota(graphene.Mutation):
    class Arguments:
        input = CreateQuotaInput(required=True)

    quota = graphene.Field(LimitedQuotaType)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: CreateQuotaInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        graphql_check_model(Quota, event.scope, info, operation="create")

        form = CreateQuotaForm(data=input.form_data)  # type: ignore
        if not form.is_valid():
            raise ValueError(form.errors)

        quota = form.save(commit=False)
        quota.event = event
        quota.save()

        quota.set_quota(form.cleaned_data["quota"])

        return CreateQuota(quota=quota)  # type: ignore
