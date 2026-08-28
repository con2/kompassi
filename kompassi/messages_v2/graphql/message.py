import graphene
import graphene_django
from graphene.types.generic import GenericScalar

from kompassi.dimensions.graphql.enums import DimensionAppType

from ..models.message import Message
from .enums import MessageDispatchType, MessageStateType
from .message_reply_to import MessageReplyToType


class MessageType(graphene_django.DjangoObjectType):
    """
    Admin-facing representation of a Message, used by the Program V2 admin compose/list
    views. Never exposed to recipients - see LimitedMessageType for the profile view.
    """

    class Meta:
        model = Message
        fields = (
            "id",
            "subject",
            "body",
            "updated_at",
            "sent_at",
            "expired_at",
        )

    app = graphene.NonNull(DimensionAppType)
    dispatch = graphene.NonNull(MessageDispatchType)
    state = graphene.NonNull(MessageStateType)
    reply_to = graphene.Field(MessageReplyToType)
    recipient_filters = graphene.NonNull(GenericScalar)

    @staticmethod
    def resolve_created_at(message: Message, info):
        return message.created_at

    created_at = graphene.NonNull(graphene.DateTime)

    @staticmethod
    def resolve_recipient_count(message: Message, info):
        """
        Number of distinct recipients (people for PER_PERSON, involvements for
        PER_INVOLVEMENT) currently matching this message's recipient filters.
        """
        return message.resolve_recipient_count()

    recipient_count = graphene.NonNull(
        graphene.Int,
        description=(resolve_recipient_count.__doc__ or "").strip(),
    )
