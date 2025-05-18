import logging

import graphene
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance
from core.utils import get_ip
from forms.models.response import Response

from ...models.invitation import Invitation
from ...models.involvement import Involvement
from ..involvement_limited import LimitedInvolvementType

logger = logging.getLogger(__name__)


class AcceptInvitationInput(graphene.InputObjectType):
    locale = graphene.String(required=True)
    event_slug = graphene.String(required=True)
    invitation_id = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class AcceptInvitation(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(AcceptInvitationInput)

    involvement = graphene.Field(LimitedInvolvementType)

    def mutate(self, info, input):
        request: HttpRequest = info.context
        if not request.user.is_authenticated:
            raise Exception("User is not authenticated")

        invitation = Invitation.objects.get(
            survey__event__slug=input.event_slug,
            id=input.invitation_id,
        )

        if invitation.used_at is not None:
            raise Exception("Invitation already used")

        survey = invitation.survey
        if not survey.is_active:
            graphql_check_instance(
                survey,
                info,
                app=survey.app,
                field="responses",
                operation="create",
            )

        event = survey.event
        if not event:
            raise Exception("Survey is not associated with an event")

        form = survey.get_form(input.locale)  # type: ignore
        if not form:
            raise Exception("Form not found")

        # TODO(https://github.com/con2/kompassi/issues/365): shows the ip of v2 backend, not the client
        ip_address = get_ip(request)

        with transaction.atomic():
            response = Response.objects.create(
                form=form,
                form_data=input.form_data,
                created_by=request.user,
                ip_address=ip_address,
                sequence_number=survey.get_next_sequence_number(),
            )
            survey.workflow.handle_new_response_phase1(response)

            invitation.mark_used()

            # TODO Should this be in Workflow?
            # However, needs the Invitation and it would not make sense for phase1 to return Involvement
            involvement = Involvement.from_accepted_invitation(
                response=response,
                invitation=invitation,
                cache=event.involvement_universe.preload_dimensions(),
            )

        survey.workflow.handle_new_response_phase2(response)
        return AcceptInvitation(involvement=involvement)  # type: ignore
