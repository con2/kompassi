import graphene
from django.db import transaction

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models.event import Event
from kompassi.involvement.models.involvement import Involvement

from ...models.message_reply_to import MessageReplyTo


class DeleteMessageReplyToInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    reply_to_id = graphene.String(required=True)


class DeleteMessageReplyTo(graphene.Mutation):
    """
    Deletes a reply-to option. Messages that reference it fall back to the event's
    default plain contact email (Message.reply_to is SET_NULL on delete).
    """

    class Arguments:
        input = DeleteMessageReplyToInput(required=True)

    reply_to_id = graphene.String()

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: DeleteMessageReplyToInput):
        event = Event.objects.get(slug=input.event_slug)

        graphql_check_model(
            Involvement, event.scope, info, app="program_v2", field="message_reply_to", operation="delete"
        )

        reply_to = MessageReplyTo.objects.get(universe=event.involvement_universe, id=input.reply_to_id)
        reply_to_id = reply_to.id
        reply_to.delete()

        return DeleteMessageReplyTo(reply_to_id=str(reply_to_id))  # type: ignore
