import graphene
from graphene_pydantic import PydanticObjectType

from core.utils.text_utils import normalize_whitespace

from ..models.profile import Profile


class SelectedProfileType(PydanticObjectType):
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

    # FMH graphene_pydantic doesn't support computed fields
    @staticmethod
    def resolve_display_name(profile: Profile, info) -> str:
        return profile.display_name

    display_name = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(Profile.display_name.__doc__ or ""),
    )

    @staticmethod
    def resolve_full_name(profile: Profile, info) -> str:
        return profile.full_name

    full_name = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(Profile.full_name.__doc__ or ""),
    )
