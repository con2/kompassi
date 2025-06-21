import graphene

from core.utils.text_utils import normalize_whitespace

from ..models.profile import Profile


class ProfileMixin:
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
