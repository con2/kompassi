import logging

import graphene
from django.db import transaction
from django.http import HttpRequest

from access.cbac import graphql_check_instance
from involvement.models.invitation import Invitation

from ...models.program import Program
from ..program_full import FullProgramType

logger = logging.getLogger(__name__)


class InviteProgramHostInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    email = graphene.String(required=True)
    language = graphene.String(required=True)


class InviteProgramHost(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(InviteProgramHostInput)

    program = graphene.NonNull(FullProgramType)

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

        with transaction.atomic():
            invitation = Invitation(
                survey=survey,
                program=program,
                email=input.email,
                created_by=request.user,
                language=input.language,
            )
            invitation.save()

        invitation.send()

        return InviteProgramHost(success=True)  # type: ignore
