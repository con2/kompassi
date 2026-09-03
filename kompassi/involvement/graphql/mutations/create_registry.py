import graphene
from django import forms as django_forms
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models.event import Event
from kompassi.core.models.organization import Organization
from kompassi.core.utils.model_utils import slugify
from kompassi.event_log_v2.utils.emit import emit

from ...dimensions import refresh_registry_dimension
from ...models.registry import Registry
from ..registry_full import FullRegistryType
from .registry_form import RegistryForm


class CreateRegistryForm(RegistryForm):
    slug = django_forms.SlugField(required=True)

    class Meta(RegistryForm.Meta):
        fields = (*RegistryForm.Meta.fields, "slug")

    def __init__(self, *args, organization: Organization, **kwargs):
        self.organization = organization
        super().__init__(*args, **kwargs)

    def clean_slug(self):
        slug = slugify(self.cleaned_data["slug"])
        if Registry.objects.filter(scope=self.organization.scope, slug=slug).exists():
            raise django_forms.ValidationError("A registry with this slug already exists.")
        return slug


class CreateRegistryInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class CreateRegistry(graphene.Mutation):
    class Arguments:
        input = CreateRegistryInput(required=True)

    registry = graphene.Field(FullRegistryType)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: CreateRegistryInput,
    ):
        request: HttpRequest = info.context

        event = Event.objects.get(slug=input.event_slug)
        organization = event.organization
        graphql_check_model(Registry, organization.scope, info, operation="create")

        form = CreateRegistryForm.from_form_data(None, input.form_data, organization=organization)  # type: ignore
        if not form.is_valid():
            raise django_forms.ValidationError(form.errors)  # type: ignore

        registry: Registry = form.save(commit=False)
        registry.scope = organization.scope
        registry.save()

        refresh_registry_dimension(organization)

        emit(
            "involvement.registry.created",
            request=request,
            organization=organization.slug,
            registry=registry.slug,
        )

        return CreateRegistry(registry=registry)  # type: ignore
