import logging

import graphene
import pydantic
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.dimensions.utils.process_dimension_value_selection_form import process_dimension_value_selection_form
from kompassi.involvement.graphql.invitation_full import FullInvitationType

from ...models.program import Program

logger = logging.getLogger(__name__)


class InviteProgramHostInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class InviteProgramHostForm(pydantic.BaseModel):
    email: str
    survey_slug: str = pydantic.Field(validation_alias="surveySlug")
    language: str


class InviteProgramHost(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(InviteProgramHostInput)

    invitation = graphene.NonNull(FullInvitationType)

    def mutate(self, info, input):
        request: HttpRequest = info.context
        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)

        if not program.can_program_host_be_invited_by(request):
            raise ValueError("Cannot invite a program host to this program.")

        values = InviteProgramHostForm.model_validate(input.form_data)
        survey = program.meta.accept_invitation_forms.get(slug=values.survey_slug)
        dimension_values = process_dimension_value_selection_form(
            program.event.involvement_universe.dimensions.filter(is_technical=False),
            input.form_data,
            slug_prefix="involvement_dimensions",
        )

        invitation = program.invite_program_host(
            email=values.email,
            survey=survey,
            language=values.language.lower(),
            involvement_dimensions=dimension_values,
        )

        return InviteProgramHost(invitation=invitation)  # type: ignore
