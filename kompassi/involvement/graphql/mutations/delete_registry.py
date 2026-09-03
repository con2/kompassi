import graphene
from django.db import transaction
from django.http import HttpRequest

from kompassi.core.models.event import Event
from kompassi.dimensions.models.dimension_value import DimensionValue
from kompassi.event_log_v2.utils.emit import emit

from ...models.registry import Registry


class DeleteRegistryInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    registry_slug = graphene.String(required=True)


class DeleteRegistry(graphene.Mutation):
    class Arguments:
        input = DeleteRegistryInput(required=True)

    slug = graphene.NonNull(graphene.String)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteRegistryInput,
    ):
        request: HttpRequest = info.context

        event = Event.objects.get(slug=input.event_slug)
        organization = event.organization
        registry = Registry.objects.get(scope=organization.scope, slug=input.registry_slug)

        if not registry.can_be_deleted_by(request):
            raise ValueError("Cannot delete registry")

        registry_slug = registry.slug
        registry.delete()

        DimensionValue.objects.filter(
            dimension__universe__scope__event__organization=organization,
            dimension__universe__slug="involvement",
            dimension__slug="registry",
            slug=registry_slug,
        ).delete()

        emit(
            "involvement.registry.deleted",
            request=request,
            organization=organization.slug,
            registry=registry_slug,
        )

        return DeleteRegistry(slug=registry_slug)  # type: ignore
