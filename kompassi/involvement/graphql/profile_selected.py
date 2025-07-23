import graphene

from kompassi.core.utils.text_utils import normalize_whitespace

from ..models.profile import Profile


class SelectedProfileType(graphene.ObjectType):
    """
    Represents a user profile with fields that can be selected for transfer.
    NOTE: Must match Profile in frontend/src/components/involvement/models.ts.
    """

    first_name = graphene.NonNull(graphene.String)
    last_name = graphene.NonNull(graphene.String)
    nick = graphene.NonNull(graphene.String)
    email = graphene.NonNull(graphene.String)
    phone_number = graphene.NonNull(graphene.String)
    discord_handle = graphene.NonNull(graphene.String)

    display_name = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(Profile.display_name.__doc__ or ""),
    )

    full_name = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(Profile.full_name.__doc__ or ""),
    )
