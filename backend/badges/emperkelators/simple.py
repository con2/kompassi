from __future__ import annotations

from typing import TYPE_CHECKING, Self

import pydantic

from badges.utils.default_badge_factory import default_badge_factory
from core.models.event import Event
from core.models.person import Person
from labour.models.personnel_class import PersonnelClass
from labour.models.signup import Signup

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
    def emperkelate(
        cls,
        event: Event,
        person: Person,
        existing_badge: Badge | None = None,
    ) -> Self:
        badge_opts = default_badge_factory(event, person)
        personnel_class: PersonnelClass | None = badge_opts.get("personnel_class")  # type: ignore

        if not personnel_class:
            return cls(override_formatted_perks="")

        signup = Signup.objects.filter(event=event, person=person).first()
        if signup and signup.override_formatted_perks:
            return cls(override_formatted_perks=signup.override_formatted_perks)

        return cls(override_formatted_perks=personnel_class.override_formatted_perks)
