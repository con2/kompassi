import graphene

from kompassi.core.utils.text_utils import normalize_whitespace

from ..models.profile import Profile
from .involvement_limited import LimitedInvolvementType
from .profile_selected import SelectedProfileType


class ProfileWithInvolvementType(SelectedProfileType):
    """
    Represents a user profile with fields describing the involvement
    of the user with an event.
    """

    involvements = graphene.NonNull(graphene.List(graphene.NonNull(LimitedInvolvementType)))

    @staticmethod
    def resolve_is_active(profile: Profile, info):
        """
        Returns True if the user has at least one active involvement in the event.
        """
        return any(involvement.is_active for involvement in profile.involvements)

    is_active = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_is_active.__doc__ or ""),
    )
