import graphene
from django.db import transaction
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.emit import emit
from kompassi.involvement.models.involvement import Involvement

from ...models.enums import MessageState
from ...models.message import Message


class DeleteMessageInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    message_id = graphene.String(required=True)


class DeleteMessage(graphene.Mutation):
    """
    Deletes a Message draft. Only drafts can be deleted - once sent, a Message is kept
    (possibly expired) so its MessageRecipients remain visible in recipients' profiles.
    """

    class Arguments:
        input = DeleteMessageInput(required=True)

    message_id = graphene.String()

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: DeleteMessageInput):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)

        graphql_check_model(Involvement, event.scope, info, app="program_v2", field="messages", operation="delete")

        message = Message.objects.get(universe=event.involvement_universe, id=input.message_id)
        if message.state != MessageState.DRAFT:
            raise ValueError("Only draft messages can be deleted")

        message_id = message.id
        message.delete()

        emit(
            "messages_v2.message.deleted",
            request=request,
            event=event,
            other_fields=dict(message_id=message_id),
        )

        return DeleteMessage(message_id=str(message_id))  # type: ignore
