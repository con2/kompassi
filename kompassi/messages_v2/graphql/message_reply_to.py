import graphene
import graphene_django

from kompassi.dimensions.graphql.enums import DimensionAppType

from ..models.message_reply_to import MessageReplyTo


class MessageReplyToType(graphene_django.DjangoObjectType):
    class Meta:
        model = MessageReplyTo
        fields = (
            "id",
            "name",
            "email",
        )

    app = graphene.NonNull(DimensionAppType)
