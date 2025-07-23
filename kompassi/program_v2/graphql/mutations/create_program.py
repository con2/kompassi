import graphene
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models import Event
from kompassi.core.utils.model_utils import slugify
from kompassi.dimensions.utils.process_dimension_value_selection_form import process_dimension_value_selection_form

from ...models.program import Program
from ..program_full import FullProgramType


class CreateProgramInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class CreateProgram(graphene.Mutation):
    class Arguments:
        input = CreateProgramInput(required=True)

    program = graphene.Field(FullProgramType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CreateProgramInput,
    ):
        # TODO scope
        event = Event.objects.get(slug=input.event_slug)
        request: HttpRequest = info.context

        graphql_check_model(
            Program,
            event.scope,
            info,
            operation="create",
        )

        values: dict[str, str] = dict(input.form_data)  # type: ignore
        slug, title, description = values.pop("slug", ""), values.pop("title", ""), values.pop("description", "")

        # They always try to use capital letters despite being told not to.
        slug = slugify(slug)

        program = Program(
            event=event,
            slug=slug,
            title=title,
            description=description,
            created_by=request.user,
        )
        program.full_clean()

        dimension_values = process_dimension_value_selection_form(
            list(event.program_universe.dimensions.filter(is_technical=False)),
            values,
        )

        with transaction.atomic():
            program.save()
            program.set_dimension_values(
                dimension_values,
                cache=event.program_universe.preload_dimensions(),
            )
            program.refresh_cached_fields()

        return CreateProgram(program=program)  # type: ignore
