import graphene
from django import forms as django_forms
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.emit import emit

from ...dimensions import refresh_registry_dimension
from ...models.registry import Registry
from ..registry_full import FullRegistryType
from .registry_form import RegistryForm


class UpdateRegistryInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    registry_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateRegistry(graphene.Mutation):
    class Arguments:
        input = UpdateRegistryInput(required=True)

    registry = graphene.Field(FullRegistryType)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: UpdateRegistryInput,
    ):
        request: HttpRequest = info.context

        event = Event.objects.get(slug=input.event_slug)
        organization = event.organization
        registry = Registry.objects.get(scope=organization.scope, slug=input.registry_slug)

        graphql_check_instance(registry, info, operation="update")

        form = RegistryForm.from_form_data(registry, input.form_data)  # type: ignore
        if not form.is_valid():
            raise django_forms.ValidationError(form.errors)  # type: ignore

        registry = form.save()

        refresh_registry_dimension(organization)

        emit(
            "involvement.registry.updated",
            request=request,
            organization=organization.slug,
            registry=registry.slug,
        )

        return UpdateRegistry(registry=registry)  # type: ignore
