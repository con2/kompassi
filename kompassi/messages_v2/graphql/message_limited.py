import graphene
import graphene_django
from graphene.types.generic import GenericScalar

from kompassi.core.graphql.event_limited import LimitedEventType

from ..models.message_recipient import MessageRecipient


class LimitedMessageType(graphene_django.DjangoObjectType):
    """
    A message as seen by its recipient in their profile: the immutable rendered
    snapshot from MessageRecipient, not the (possibly since-edited) Message. Carries no
    sender identity.
    """

    class Meta:
        model = MessageRecipient
        fields = (
            "id",
            "subject",
            "sent_at",
        )

    cached_dimensions = graphene.NonNull(GenericScalar)
    event = graphene.NonNull(LimitedEventType)
    body_html = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_event(recipient: MessageRecipient, info):
        return recipient.message.event

    @staticmethod
    def resolve_body_html(recipient: MessageRecipient, info):
        return recipient.body.text
