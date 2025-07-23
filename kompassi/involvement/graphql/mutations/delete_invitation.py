import logging

import graphene

from kompassi.access.cbac import graphql_check_instance

from ...models.invitation import Invitation
from ..invitation_limited import LimitedInvitationType

logger = logging.getLogger(__name__)


class DeleteInvitationInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    invitation_id = graphene.String(required=True)


class DeleteInvitation(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(DeleteInvitationInput)

    invitation = graphene.Field(LimitedInvitationType)

    def mutate(self, info, input):
        invitation = Invitation.objects.get(
            survey__event__slug=input.event_slug,
            id=input.invitation_id,
        )

        graphql_check_instance(
            invitation,
            info,
            app=invitation.survey.app_name,
            operation="delete",
        )

        if invitation.used_at is not None:
            raise Exception("Invitation already used or revoked")

        invitation.mark_used()

        return DeleteInvitation(invitation=invitation)  # type: ignore
