from involvement.models.involvement import Involvement

from .profile import Profile


class ProfileWithInvolvement(
    Profile,
    frozen=True,
    populate_by_name=True,
    allow_arbitrary_types=True,
):
    involvements: list[Involvement]
