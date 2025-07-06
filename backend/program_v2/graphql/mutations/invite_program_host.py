import logging

import graphene
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from dimensions.models.cached_dimensions import validate_cached_dimensions
from involvement.graphql.invitation_full import FullInvitationType

from ...models.program import Program

logger = logging.getLogger(__name__)


class InviteProgramHostInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)  # if we ever want to have multiple acceptance forms
    email = graphene.String(required=True)
    language = graphene.String(required=True)
    dimension_values = GenericScalar()


class InviteProgramHost(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(InviteProgramHostInput)

    invitation = graphene.NonNull(FullInvitationType)

    def mutate(self, info, input):
        request: HttpRequest = info.context
        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)

        if not program.can_program_host_be_invited_by(request):
            raise ValueError("Cannot invite a program host to this program.")

        survey = program.meta.accept_invitation_forms.get(slug=input.survey_slug)

        dimension_values = validate_cached_dimensions(input.dimension_values) if input.dimension_values else {}

        invitation = program.invite_program_host(
            email=input.email,
            survey=survey,
            language=input.language.lower(),
            involvement_dimensions=dimension_values,
        )

        return InviteProgramHost(invitation=invitation)  # type: ignore
