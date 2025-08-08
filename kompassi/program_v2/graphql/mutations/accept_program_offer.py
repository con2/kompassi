import graphene
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance, graphql_check_model
from kompassi.core.models.event import Event
from kompassi.dimensions.utils.process_dimension_value_selection_form import process_dimension_value_selection_form
from kompassi.forms.models.field import Field, FieldType
from kompassi.forms.utils.process_form_data import process_form_data

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
        request: HttpRequest = info.context
        form_data: dict[str, str] = input.form_data  # type: ignore
        event = Event.objects.get(slug=input.event_slug)
        meta = event.program_v2_event_meta
        if not meta:
            raise ValueError("Event is not a program event")

        program_offer = meta.current_program_offers.get(id=input.response_id)

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

        program_dimensions = process_dimension_value_selection_form(
            list(event.program_universe.dimensions.filter(is_technical=False)),
            form_data,
            slug_prefix="program_dimensions",
        )
        involvement_dimensions = process_dimension_value_selection_form(
            list(event.involvement_universe.dimensions.filter(is_technical=False)),
            form_data,
            slug_prefix="involvement_dimensions",
        )

        program = Program.from_program_offer(
            program_offer,
            slug=values.get("slug", ""),
            title=values.get("title", ""),
            created_by=request.user,
            program_dimension_values=program_dimensions,
            involvement_dimension_values=involvement_dimensions,
        )

        return AcceptProgramOffer(program=program)  # type: ignore
