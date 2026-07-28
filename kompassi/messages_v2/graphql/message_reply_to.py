import graphene
import graphene_django

from ..models.message_reply_to import MessageReplyTo
from .enums import MessageAppType


class MessageReplyToType(graphene_django.DjangoObjectType):
    class Meta:
        model = MessageReplyTo
        fields = (
            "id",
            "name",
            "email",
        )

    app = graphene.NonNull(MessageAppType)
