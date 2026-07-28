import graphene
from django.db import transaction

from kompassi.access.cbac import graphql_check_model
from kompassi.core.models.event import Event
from kompassi.involvement.models.involvement import Involvement

from ...models.message_reply_to import MessageReplyTo
from ..message_reply_to import MessageReplyToType


class CreateMessageReplyToInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    name = graphene.String(required=True)
    email = graphene.String(required=True)


class CreateMessageReplyTo(graphene.Mutation):
    class Arguments:
        input = CreateMessageReplyToInput(required=True)

    reply_to = graphene.Field(MessageReplyToType)

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: CreateMessageReplyToInput):
        event = Event.objects.get(slug=input.event_slug)

        graphql_check_model(
            Involvement, event.scope, info, app="program_v2", field="message_reply_to", operation="create"
        )

        reply_to = MessageReplyTo.objects.create(
            universe=event.involvement_universe,
            name=input.name,
            email=input.email,
        )

        return CreateMessageReplyTo(reply_to=reply_to)  # type: ignore
