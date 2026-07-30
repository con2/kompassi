import graphene
from django.db import transaction
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.emit import emit
from kompassi.involvement.models.involvement import Involvement

from ...models.message import Message
from ...models.message_reply_to import MessageReplyTo
from ..enums import MessageDispatchType
from ..message import MessageType


class CreateMessageInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    subject = graphene.String(required=True)
    body = graphene.String(required=True)
    dispatch = graphene.Argument(MessageDispatchType, required=True)
    reply_to_id = graphene.String()
    # list[list[{dimension: str, values: list[str] | null}]] - OR of AND-groups.
    recipient_filters = GenericScalar(required=True)


class CreateMessage(graphene.Mutation):
    """
    Creates a new Message with the given content. Called only when the compose view
    for a not-yet-existing message ("new") is first saved - until then, the draft only
    exists in the browser, never in the database.
    """

    class Arguments:
        input = CreateMessageInput(required=True)

    message = graphene.Field(MessageType)

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: CreateMessageInput):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)
        universe = event.involvement_universe

        graphql_check_model(Involvement, event.scope, info, app="program_v2", field="messages", operation="create")

        message = Message(
            universe=universe,
            created_by=request.user,
            subject=input.subject,
            body=input.body,
            dispatch=input.dispatch,
            reply_to=MessageReplyTo.from_untrusted(
                universe,
                input.reply_to_id,  # type: ignore
            ),
            recipient_filters=input.recipient_filters or [],
        )
        message.clean_recipient_filters()
        message.save()

        emit(
            "messages_v2.message.created",
            request=request,
            event=event,
            other_fields=dict(message_id=message.id),
        )

        return CreateMessage(message=message)  # type: ignore
