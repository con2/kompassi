import graphene
from graphene_pydantic import PydanticObjectType

from ..models.profile_with_involvement import ProfileWithInvolvement
from .involvement_limited import LimitedInvolvementType
from .profile_mixin import ProfileMixin


class ProfileWithInvolvementType(ProfileMixin, PydanticObjectType):
    """
    Represents a user profile with fields describing the involvement
    of the user with an event.
    """

    class Meta:
        model = ProfileWithInvolvement
        fields = (
            "first_name",
            "last_name",
            "nick",
            "email",
            "phone_number",
            "discord_handle",
            "involvements",
        )

    involvements = graphene.NonNull(graphene.List(graphene.NonNull(LimitedInvolvementType)))
