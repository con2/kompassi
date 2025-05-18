import graphene
import graphene_django

from ..models.invitation import Invitation


class LimitedInvitationType(graphene_django.DjangoObjectType):
    class Meta:
        model = Invitation
        fields = (
            "id",
            "survey",
            "language",
        )

    @staticmethod
    def resolve_is_used(invitation: Invitation, info) -> bool:
        return invitation.used_at is not None

    is_used = graphene.NonNull(graphene.Boolean)
