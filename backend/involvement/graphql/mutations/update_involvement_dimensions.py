import graphene
from django.db import transaction
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.models import Event
from dimensions.utils.process_dimension_value_selection_form import process_dimension_value_selection_form

from ...models.involvement import Involvement
from ..involvement_limited import LimitedInvolvementType


class UpdateInvolvementDimensionsInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    involvement_id = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateInvolvementDimensions(graphene.Mutation):
    class Arguments:
        input = UpdateInvolvementDimensionsInput(required=True)

    involvement = graphene.Field(LimitedInvolvementType)

    @transaction.atomic
    @staticmethod
    def mutate(
        _root,
        info,
        input: UpdateInvolvementDimensionsInput,
    ):
        form_data: dict[str, str] = input.form_data  # type: ignore

        involvement = Involvement.objects.get(event__slug=input.event_slug, slug=input.involvement_id)
        event: Event = involvement.event
        universe = event.involvement_universe

        dimensions = list(universe.dimensions.filter(is_technical=False))

        graphql_check_instance(
            involvement,  # type: ignore
            info,
            field="dimensions",
            operation="update",
            app=involvement.app.app_name,
        )

        values = process_dimension_value_selection_form(dimensions, form_data)
        cache = universe.preload_dimensions(dimension_slugs=values.keys())
        involvement.set_dimension_values(values, cache=cache)
        involvement.refresh_cached_dimensions()
        involvement.refresh_dependents()

        return UpdateInvolvementDimensions(Involvement=Involvement)  # type: ignore
