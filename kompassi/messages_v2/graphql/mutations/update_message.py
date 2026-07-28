import graphene
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.emit import emit
from kompassi.involvement.models.involvement import Involvement

from ...models.message import Message
from ..enums import MessageDispatchType
from ..message import MessageType


class UpdateMessageInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    message_id = graphene.String(required=True)
    subject = graphene.String(required=True)
    body = graphene.String(required=True)
    dispatch = graphene.Argument(MessageDispatchType, required=True)
    reply_to_id = graphene.String()
    # list[list[{dimension: str, values: list[str] | null}]] - OR of AND-groups.
    recipient_filters = GenericScalar(required=True)


class UpdateMessage(graphene.Mutation):
    """
    Updates a Message's subject/body/dispatch/reply-to/recipient filters. Works on a
    Message in any state, including ACTIVE (already sent) - edits are not retroactive:
    existing MessageRecipient rows keep their immutable rendered snapshot, and the
    updated content only applies to recipients who receive it from now on (subsequent
    explicit re-sends and the auto-send hook for newly-matching involvements).
    """

    class Arguments:
        input = UpdateMessageInput(required=True)

    message = graphene.Field(MessageType)

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: UpdateMessageInput):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)

        graphql_check_model(Involvement, event.scope, info, app="program_v2", field="messages", operation="update")

        message = Message.objects.get(universe=event.involvement_universe, id=input.message_id)

        message.subject = input.subject
        message.body = input.body
        message.dispatch = input.dispatch
        message.reply_to_id = input.reply_to_id or None
        message.recipient_filters = input.recipient_filters or []
        message.clean_recipient_filters()
        message.save()

        emit(
            "messages_v2.message.edited",
            request=request,
            event=event,
            other_fields=dict(message_subject=message.subject or "(no subject)"),
        )

        return UpdateMessage(message=message)  # type: ignore
