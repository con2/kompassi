from graphene_pydantic import PydanticObjectType

from ..models.profile import Profile
from .profile_mixin import ProfileMixin


class SelectedProfileType(ProfileMixin, PydanticObjectType):
    """
    Represents a user profile with fields that can be selected for transfer.
    NOTE: Must match Profile in frontend/src/components/involvement/models.ts.
    """

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "nick",
            "email",
            "phone_number",
            "discord_handle",
        )
