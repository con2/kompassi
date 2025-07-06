import graphene
from django.db import transaction
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.models.event import Event
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

        # while involvement_id would suffice and event_slug is not strictly necessary,
        # we want to validate event_slug because the caller will use it in redirects
        event = Event.objects.get(slug=input.event_slug)
        universe = event.involvement_universe
        involvement = Involvement.objects.get(universe=universe, id=input.involvement_id)
        graphql_check_instance(
            involvement,  # type: ignore
            info,
            field="dimensions",
            operation="update",
            app=involvement.app.app_name,
        )

        universe = involvement.universe
        values = process_dimension_value_selection_form(universe.dimensions.filter(is_technical=False), form_data)
        cache = universe.preload_dimensions(dimension_slugs=values.keys())
        involvement.set_dimension_values(values, cache=cache)
        involvement.refresh_cached_dimensions()
        involvement.refresh_dependents()

        return UpdateInvolvementDimensions(involvement=involvement)  # type: ignore
