import graphene
from django.db import transaction
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance, graphql_check_model
from core.models.event import Event
from dimensions.utils.process_dimensions_form import process_dimensions_form
from forms.models.field import Field, FieldType
from forms.models.response import Response
from forms.utils.process_form_data import process_form_data

from ...models.program import Program
from ..program_full import FullProgramType

# TODO supply system forms to the frontend from the backend
ACCEPT_PROGRAM_FORM_FIELDS = [
    Field(
        slug="slug",
        type=FieldType.SINGLE_LINE_TEXT,
        required=True,
    ),
    Field(
        slug="title",
        type=FieldType.SINGLE_LINE_TEXT,
        required=False,
    ),
    # dimensions are added dynamically
]


class AcceptProgramOfferInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    response_id = graphene.UUID(required=True)
    form_data = GenericScalar(required=True)


class AcceptProgramOffer(graphene.Mutation):
    class Arguments:
        input = AcceptProgramOfferInput(required=True)

    program = graphene.NonNull(FullProgramType)

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: AcceptProgramOfferInput):
        """
        Turns a program offer into a program.
        """
        form_data: dict[str, str] = input.form_data  # type: ignore

        program_offer = Response.objects.get(
            id=input.response_id,
            form__event__slug=input.event_slug,
            form__survey__app="program_v2",
        )
        event: Event = program_offer.form.event  # ugh

        # check that we are both allowed to read the program offer and create a program
        graphql_check_instance(
            program_offer,
            info,
            app="program_v2",
        )
        graphql_check_model(
            Program,
            event.scope,
            info,
            operation="create",
        )

        # NOTE form_data is the form sent when accepting the program offer
        # and not the form sent when creating the program offer
        values, warnings = process_form_data(ACCEPT_PROGRAM_FORM_FIELDS, form_data)
        if warnings:
            raise ValueError(warnings)

        dimension_values = process_dimensions_form(
            list(event.program_universe.dimensions.all()),
            form_data,
        )
        program_offer.set_dimension_values(dimension_values)

        program = Program.from_program_offer(
            program_offer,
            slug=values["slug"],
            title=values.get("title", ""),
        )
        program.set_dimension_values(dimension_values)
        program.refresh_cached_fields()

        return AcceptProgramOffer(program=program)  # type: ignore
