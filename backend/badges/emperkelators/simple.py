from __future__ import annotations

from typing import TYPE_CHECKING, Self

import pydantic

if TYPE_CHECKING:
    from ..models.badge import Badge


class SimpleEmperkelator(pydantic.BaseModel):
    """
    Assumes perks are recorded in PersonnelClass.override_formatted_perks
    and gives the perks of the personnel class indicated by the default badge factory.
    No stacking of perks is done.
    """

    override_formatted_perks: str = ""

    def __str__(self):
        return self.override_formatted_perks

    @classmethod
    def emperkelate(cls, badge: Badge) -> Self:
        if not badge.person:
            return cls()

        signup = badge.signup
        if signup and signup.override_formatted_perks:
            return cls(override_formatted_perks=signup.override_formatted_perks)

        return cls(override_formatted_perks=badge.personnel_class.override_formatted_perks)
