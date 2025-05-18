import logging

import graphene
from django.http import HttpRequest

from access.cbac import graphql_check_instance
from involvement.graphql.invitation_full import FullInvitationType

from ...models.program import Program

logger = logging.getLogger(__name__)


class InviteProgramHostInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)  # if we ever want to have multiple acceptance forms
    email = graphene.String(required=True)
    language = graphene.String(required=True)


class InviteProgramHost(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(InviteProgramHostInput)

    invitation = graphene.NonNull(FullInvitationType)

    def mutate(self, info, input):
        request: HttpRequest = info.context
        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)

        graphql_check_instance(
            program,
            request,
            field="program_hosts",
            operation="create",
        )

        survey = program.meta.accept_invitation_forms.get(slug=input.survey_slug)

        invitation = program.invite_program_host(
            email=input.email,
            survey=survey,
            language=input.language.lower(),
        )

        return InviteProgramHost(invitation=invitation)  # type: ignore
