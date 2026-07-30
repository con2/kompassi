import graphene
from django.db import transaction
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.emit import emit
from kompassi.involvement.models.involvement import Involvement

from ...models.message import Message
from ..message import MessageType


class SendMessageInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    message_id = graphene.String(required=True)


class SendMessage(graphene.Mutation):
    """
    Sends a Message: on a draft, transitions it to ACTIVE and dispatches sending to all
    currently matching recipients. On an already ACTIVE message, this re-sends to any
    currently matching recipients who have not yet received it (MessageRecipient's
    uniqueness constraints make this idempotent for everyone else).
    """

    class Arguments:
        input = SendMessageInput(required=True)

    message = graphene.Field(MessageType)

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: SendMessageInput):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)

        graphql_check_model(Involvement, event.scope, info, app="program_v2", field="messages", operation="update")

        message = Message.objects.get(universe=event.involvement_universe, id=input.message_id)
        was_draft = message.sent_at is None
        initial_recipients = message.resolve_recipient_count()
        message.send()

        if was_draft:
            # "sent" is emitted only once, on the draft -> active transition (never
            # on a subsequent explicit re-send), and never carries recipient emails.
            emit(
                "messages_v2.message.sent",
                request=request,
                event=event,
                other_fields=dict(
                    message_id=message.id,
                    initial_recipients=initial_recipients,
                ),
            )

        return SendMessage(message=message)  # type: ignore
