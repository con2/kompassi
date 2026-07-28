import graphene
from django.db import transaction
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.emit import emit
from kompassi.involvement.models.involvement import Involvement

from ...models.message import Message
from ..message import MessageType


class ExpireMessageInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    message_id = graphene.String(required=True)


class ExpireMessage(graphene.Mutation):
    """
    Expires an active Message: it stops being sent to new/auto-matching recipients.
    People who already received it are unaffected.
    """

    class Arguments:
        input = ExpireMessageInput(required=True)

    message = graphene.Field(MessageType)

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: ExpireMessageInput):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)

        graphql_check_model(Involvement, event.scope, info, app="program_v2", field="messages", operation="update")

        message = Message.objects.get(universe=event.involvement_universe, id=input.message_id)
        message.expire()

        emit(
            "messages_v2.message.expired",
            request=request,
            event=event,
            other_fields=dict(message_subject=message.subject or "(no subject)"),
        )

        return ExpireMessage(message=message)  # type: ignore
