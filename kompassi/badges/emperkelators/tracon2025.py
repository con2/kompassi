from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel

from kompassi.badges.models.survey_to_badge import SurveyToBadgeMapping
from kompassi.zombies.programme.models.programme_role import ProgrammeRole

if TYPE_CHECKING:
    from ..models.badge import Badge

THIRD_MEAL_MIN_HOURS = 12
FOURTH_MEAL_MIN_HOURS = 16
EXTRA_SWAG_MIN_HOURS = 14
MAX_MEALS = 4


class TicketType(IntEnum):
    NONE = 0
    MAY_BUY = 1
    DAY_TICKET = 2
    WEEKEND_TICKET = 3
    EXTERNAL_BADGE = 4
    INTERNAL_BADGE = 5
    SUPER_INTERNAL_BADGE = 6

    def __str__(self):
        match self:
            case TicketType.NONE:
                return "Ei lippuetua"
            case TicketType.MAY_BUY:
                return "Voi ostaa lipun"
            case TicketType.DAY_TICKET:
                return "Päivälippu"
            case TicketType.WEEKEND_TICKET:
                return "Viikonloppulippu"
            case TicketType.EXTERNAL_BADGE:
                return "Badge (external)"
            case TicketType.INTERNAL_BADGE:
                return "Badge (internal)"
            case TicketType.SUPER_INTERNAL_BADGE:
                return "Badge (super internal)"


class Tracon2025Emperkelator(BaseModel):
    ticket_type: TicketType = TicketType.NONE
    meals: int = 0
    swag: bool = False
    extra_swag: bool = False
    override_formatted_perks: str = ""

    def imbibe(self, perks: Self) -> Self:
        """
        Combine two sources of perks for the same person.
        This is the Plus (+) operator in the additive monoid of Perks.
        """
        self.ticket_type = max(self.ticket_type, perks.ticket_type)
        self.meals = min(self.meals + perks.meals, MAX_MEALS)
        self.swag |= perks.swag
        self.extra_swag |= perks.extra_swag

        if perks.override_formatted_perks:
            if self.override_formatted_perks:
                raise ValueError("Don't know how to combine two override_formatted_perks")
            self.override_formatted_perks = perks.override_formatted_perks

        return self

    def __str__(self):
        if self.override_formatted_perks:
            return self.override_formatted_perks

        match self.meals:
            case 0:
                meals = "ei ruokalippuja"
            case 1:
                meals = "1 ruokalippu"
            case n:
                meals = f"{n} ruokalippua"

        match (self.swag, self.extra_swag):
            case (False, False):
                swag = "ei työvoimatuotteita"
            case (True, False):
                swag = "valittu työvoimatuote"
            case (False, True):
                # this shouldn't happen (extra_swag without swag) but for completeness
                swag = "kangaskassi"
            case (True, True):
                swag = "valittu työvoimatuote ja ekstrakangaskassi"

        return f"{self.ticket_type}, {meals}, {swag}"

    @classmethod
    def emperkelate(cls, badge: Badge) -> Self:
        if not badge.person:
            return cls()

        # XXX This must die in a fire. Involvement to the Rescue.
        if badge.personnel_class.slug == "taidekuja":
            for mapping in (
                SurveyToBadgeMapping.objects.filter(
                    survey__event=badge.event,
                    survey__slug="artist-alley-application",
                )
                .select_related("personnel_class")
                .order_by("priority")
            ):
                if mapping.match(badge.person):
                    return cls(
                        override_formatted_perks=mapping.annotations.get("tracon2025:formattedPerks", ""),
                    )

        perks = cls()
        extra_meal_token = cls(meals=1)
        extra_swag = cls(extra_swag=True)

        signup = badge.signup
        if signup:
            if signup.override_formatted_perks:
                return cls(override_formatted_perks=signup.override_formatted_perks)
            elif personnel_class := signup.personnel_class:
                pc_perks = cls.model_validate(personnel_class.perks)
                perks.imbibe(pc_perks)
                hours = signup.working_hours

                if hours >= THIRD_MEAL_MIN_HOURS:
                    perks.imbibe(extra_meal_token)
                if hours >= FOURTH_MEAL_MIN_HOURS:
                    perks.imbibe(extra_meal_token)

                if hours >= EXTRA_SWAG_MIN_HOURS:
                    perks.imbibe(extra_swag)

        for programme_role in ProgrammeRole.objects.filter(programme__category__event=badge.event, person=badge.person):
            programme_perks = cls.model_validate(programme_role.perks)
            perks.imbibe(programme_perks)

        return perks
