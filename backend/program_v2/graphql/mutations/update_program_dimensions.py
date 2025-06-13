import graphene
from django.db import transaction
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.models import Event
from dimensions.utils.process_dimensions_form import process_dimensions_form

from ...models.program import Program
from ..program_full import FullProgramType


class UpdateProgramDimensionsInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class UpdateProgramDimensions(graphene.Mutation):
    class Arguments:
        input = UpdateProgramDimensionsInput(required=True)

    program = graphene.Field(FullProgramType)

    @transaction.atomic
    @staticmethod
    def mutate(
        _root,
        info,
        input: UpdateProgramDimensionsInput,
    ):
        form_data: dict[str, str] = input.form_data  # type: ignore

        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)
        event: Event = program.event
        universe = event.program_universe

        dimensions = list(universe.dimensions.filter(is_technical=False))

        graphql_check_instance(
            program,
            info,
            field="dimensions",
            operation="update",
        )

        values = process_dimensions_form(dimensions, form_data)
        cache = universe.preload_dimensions(dimension_slugs=values.keys())
        program.set_dimension_values(values, cache=cache)
        program.refresh_cached_dimensions()
        program.refresh_dependents()

        return UpdateProgramDimensions(program=program)  # type: ignore
