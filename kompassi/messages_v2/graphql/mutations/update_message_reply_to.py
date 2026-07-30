import graphene
from django.core.validators import validate_email
from django.db import transaction

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models.event import Event
from kompassi.involvement.models.involvement import Involvement

from ...models.message_reply_to import MessageReplyTo
from ..message_reply_to import MessageReplyToType


class UpdateMessageReplyToInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    reply_to_id = graphene.String(required=True)
    name = graphene.String(required=True)
    email = graphene.String(required=True)


class UpdateMessageReplyTo(graphene.Mutation):
    class Arguments:
        input = UpdateMessageReplyToInput(required=True)

    reply_to = graphene.Field(MessageReplyToType)

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: UpdateMessageReplyToInput):
        event = Event.objects.get(slug=input.event_slug)

        graphql_check_model(
            Involvement, event.scope, info, app="program_v2", field="message_reply_to", operation="update"
        )

        validate_email(input.email)

        reply_to = MessageReplyTo.objects.get(universe=event.involvement_universe, id=input.reply_to_id)
        reply_to.name = input.name
        reply_to.email = input.email
        reply_to.save()

        return UpdateMessageReplyTo(reply_to=reply_to)  # type: ignore
