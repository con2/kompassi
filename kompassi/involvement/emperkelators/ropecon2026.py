from __future__ import annotations

import logging
from datetime import timedelta
from enum import Enum
from functools import cached_property

import pydantic

from kompassi.core.models.event import Event
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.dimensions.models.dimension_dto import DimensionDTO
from kompassi.dimensions.models.dimension_value_dto import DimensionValueDTO
from kompassi.dimensions.models.enums import AnnotationDataType, ValueOrdering

from ..models.enums import InvolvementType
from ..models.involvement import Involvement
from .base import BaseEmperkelator

logger = logging.getLogger(__name__)


class TicketType(Enum):
    """
    Ropecon tracks ticket and badge types separately.
    Program hosts may get either a day ticket or a weekend ticket, depending on the number and total duration of program.
    Volunteers always get a weekend ticket.
    """

    title_fi: str
    title_en: str

    NONE = "none", "Ei lippuetua", "No ticket benefit"
    DAY_TICKET = "day-ticket", "Päivälippu", "Day ticket"
    WEEKEND_TICKET = "weekend-ticket", "Viikonloppulippu", "Weekend ticket"

    @classmethod
    def as_dimension_dto(cls) -> DimensionDTO:
        return DimensionDTO(
            slug="ticket-type",
            title=dict(
                en="Ticket type",
                fi="Lipputyyppi",
            ),
            choices=[
                DimensionValueDTO(
                    slug=tt.value,
                    title=dict(
                        en=tt.title_en,
                        fi=tt.title_fi,
                    ),
                )
                for tt in cls
                if tt != cls.NONE
            ],
            value_ordering=ValueOrdering.MANUAL,
        )

    def combine(self, other: TicketType) -> TicketType:
        return max(self, other)

    def __new__(cls, value: str, title_fi: str, title_en: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title_fi = title_fi
        obj.title_en = title_en
        return obj

    def __lt__(self, other: TicketType) -> bool:
        return TICKET_TYPES.index(self) < TICKET_TYPES.index(other)


# for use only by __lt__, others should iterate over TicketType
TICKET_TYPES = list(TicketType)


class BadgeType(Enum):
    v1_personnel_class_slug: str | None
    title_fi: str
    title_en: str

    NONE = "none", None, "Ei badgea", "No badge"
    PROGRAM_BADGE = "program", "ohjelma", "Ohjelmabadge", "Program host badge"
    VOLUNTEER_BADGE = "volunteer", "tyovoima", "Vapaaehtoisbadge", "Volunteer badge"
    OVERSEER_BADGE = "overseer", "ylivankari", "Ylivänkäribadge", "Overseer badge"
    ORGANIZER_BADGE = "organizer", "conitea", "Coniteabadge", "Organizer badge"

    def __new__(cls, value: str, v1_personnel_class_slug: str | None, title_fi: str, title_en: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.v1_personnel_class_slug = v1_personnel_class_slug
        obj.title_fi = title_fi
        obj.title_en = title_en
        return obj

    def __lt__(self, other: BadgeType) -> bool:
        return BADGE_TYPES.index(self) < BADGE_TYPES.index(other)


# for use only by __lt__, others should iterate over BadgeType
BADGE_TYPES = list(BadgeType)


class Rule(Enum):
    """
    Explains to the user why they have the perks they have.
    This is not used for any logic, only for display purposes.
    """

    title_fi: str
    title_en: str

    NONE = "none", "Ei sääntöä", "No rule"
    V1_CONCOM = "v1-concom", "Työvoima V1: Conitea", "Labour V1: Concom"
    V1_OVERSEER = "v1-overseer", "Työvoima V1: Ylivänkäri", "Labour V1: Overseer"
    V1_VOLUNTEER = "v1-volunteer", "Työvoima V1: Vapaaehtoinen", "Labour V1: Volunteer"
    V1_NO_MATCH = "v1-no-match", "Työvoima V1: Mikään sääntö ei sovellu", "Labour V1: No rule matches"
    PROGRAM_HOST_2_OR_MORE = (
        "program-host-2-or-more",
        "Päävastuullinen väh. 2 aikataulumerkinnässä",
        "Main program host in two or more schedule items",
    )
    PROGRAM_HOST_1_OVER_6H = (
        "program-host-1-over-6h",
        "Päävastuullinen 1 aikataulumerkinnässä, joka kestää väh. 6h",
        "Main program host in one schedule item of 6 hours or more",
    )
    PROGRAM_HOST_1_AND_HELPER_1 = (
        "program-host-1-and-helper-1",
        "Päävastuullinen 1 aikataulumerkinnässä ja ohjelma-apuri toisessa",
        "Main program host in one schedule item and helper in another",
    )
    PROGRAM_HOST_1 = (
        "program-host-1",
        "Päävastuullinen 1 aikataulumerkinnässä",
        "Main program host in one schedule item",
    )
    PROGRAM_HELPER_2_OR_MORE = (
        "program-helper-2-or-more",
        "Ohjelma-apuri väh. 2 aikataulumerkinnässä",
        "Program helper in two or more schedule items",
    )
    PROGRAM_HELPER_1 = (
        "program-helper-1",
        "Ohjelma-apuri 1 aikataulumerkinnässä",
        "Program helper in one schedule item",
    )
    PROGRAM_NO_MATCH = (
        "program-no-match",
        "Ohjelmanjärjestäjä, johon mikään tarkempi sääntö ei sovellu",
        "Program host that does not match any more specific rule",
    )

    @classmethod
    def as_dimension_dto(cls) -> DimensionDTO:
        return DimensionDTO(
            slug="perks-rule",
            title=dict(
                en="Perks rule",
                fi="Etusääntö",
            ),
            # description=dict(
            #     en="Identifies the rule that was used to determine the perks for this person",
            #     fi="Kertoo säännön, jota käytettiin tämän henkilön etujen määrittämiseen",
            # ),
            choices=[
                DimensionValueDTO(
                    slug=tt.value,
                    title=dict(
                        en=tt.title_en,
                        fi=tt.title_fi,
                    ),
                )
                for tt in cls
                if tt != cls.NONE
            ],
            value_ordering=ValueOrdering.MANUAL,
        )

    def __new__(cls, value: str, title_fi: str, title_en: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title_fi = title_fi
        obj.title_en = title_en
        return obj


class Perks(pydantic.BaseModel):
    badge_type: BadgeType = BadgeType.NONE
    ticket_type: TicketType = TicketType.NONE
    meals: int = 0
    override_formatted_perks: str = ""
    rule: Rule = Rule.NONE

    @property
    def formatted_perks(self) -> str:
        if self.override_formatted_perks:
            return self.override_formatted_perks

        parts = []

        if self.ticket_type != TicketType.NONE:
            parts.append(self.ticket_type.title_fi)

        if self.badge_type != BadgeType.NONE:
            parts.append(self.badge_type.title_fi.lower())

        if self.meals == 1:
            parts.append("1 ruokalippu")
        elif self.meals > 1:
            parts.append(f"{self.meals} ruokalippua")

        return ", ".join(parts)

    @classmethod
    def for_v1_signup(cls, involvement: Involvement) -> Perks:
        if involvement.type != InvolvementType.LEGACY_SIGNUP:
            raise ValueError(f"Expected involvement type {InvolvementType.LEGACY_SIGNUP}, got {involvement.type}")
        if involvement.signup is None:
            raise ValueError("Expected involvement to have a signup, but it was None")

        personnel_classes = set(involvement.signup.personnel_classes.values_list("slug", flat=True))
        if "conitea" in personnel_classes:
            ticket_type = TicketType.WEEKEND_TICKET
            badge_type = BadgeType.ORGANIZER_BADGE
            meals = 2
            rule = Rule.V1_CONCOM
        elif "tyovoima" in personnel_classes or "ylivankari" in personnel_classes or "ylityovoima" in personnel_classes:
            ticket_type = TicketType.WEEKEND_TICKET
            badge_type = BadgeType.VOLUNTEER_BADGE
            meals = 2
            rule = Rule.V1_VOLUNTEER
        else:
            ticket_type = TicketType.NONE
            badge_type = BadgeType.NONE
            meals = 0
            rule = Rule.V1_NO_MATCH

        return Perks(
            ticket_type=ticket_type,
            badge_type=badge_type,
            meals=meals,
            override_formatted_perks=involvement.signup.override_formatted_perks,
            rule=rule,
        )

    @classmethod
    def for_program_host(cls, ticket_type: TicketType, meals: int, rule: Rule) -> Perks:
        return Perks(
            badge_type=BadgeType.PROGRAM_BADGE,
            ticket_type=ticket_type,
            meals=meals,
            rule=rule,
        )


def extract_schedule_items_from_involvements(involvements: list[Involvement]) -> list:
    schedule_items = []
    for involvement in involvements:
        if involvement.program:
            schedule_items.extend(involvement.program.schedule_items.all())
    return schedule_items


class RopeconEmperkelator(BaseEmperkelator):
    @cached_property
    def perks(self) -> Perks:
        if (
            v1_signup := next((i for i in self.involvements if i.type == InvolvementType.LEGACY_SIGNUP), None)
        ) is not None:
            return Perks.for_v1_signup(v1_signup)

        program_involvements = [i for i in self.involvements if i.type == InvolvementType.PROGRAM_HOST]
        main_involvements = [
            i for i in program_involvements if i.response and i.response.survey.slug != "offer-program-hosts"
        ]
        main_schedule_items = extract_schedule_items_from_involvements(main_involvements)

        six_hours = timedelta(hours=6)
        main_program_host_involvements_over6h = [
            i
            for i in main_involvements
            if i.program and i.program.schedule_items.filter(duration__gte=six_hours).exists()
        ]
        main_program_host_schedule_items_over6h = extract_schedule_items_from_involvements(
            main_program_host_involvements_over6h
        )
        helper_involvements = [
            i for i in program_involvements if i.response and i.response.survey.slug == "offer-program-hosts"
        ]
        helper_schedule_items = extract_schedule_items_from_involvements(helper_involvements)

        # päävastuullinen vähintään 2 aikataulumerkinnässä TAI
        # päävastuullinen yhdessä aikataulumerkinnässä, joka kestää 6 h tai enemmän TAI
        # päävastuullinen yhdessä aikataulumerkinnässä ja ohjelma-apuri jossain muussa ohjelmassa -> viikonloppulippu + 1 ruokalippu
        if (
            len(main_schedule_items) >= 2
            or len(main_program_host_schedule_items_over6h) > 0
            or (len(main_schedule_items) == 1 and len(helper_schedule_items) > 0)
        ):
            return Perks.for_program_host(
                ticket_type=TicketType.WEEKEND_TICKET,
                meals=1,
                rule=Rule.PROGRAM_HOST_2_OR_MORE,
            )

        # päävastuullinen yhdessä aikataulumerkinnässä -> päivälippu + 1 ruokalippu
        if len(main_schedule_items) == 1:
            return Perks.for_program_host(
                ticket_type=TicketType.DAY_TICKET,
                meals=1,
                rule=Rule.PROGRAM_HOST_1,
            )

        # ohjelma-apuri vähintään 2 aikataulumerkinnässä -> viikonloppulippu (ei ruokaa)
        if len(helper_schedule_items) >= 2:
            return Perks.for_program_host(
                ticket_type=TicketType.WEEKEND_TICKET,
                meals=0,
                rule=Rule.PROGRAM_HELPER_2_OR_MORE,
            )

        # ohjelma-apuri yhdessä aikataulumerkinnässä -> päivälippu (ei ruokaa)
        if len(helper_schedule_items) == 1:
            return Perks.for_program_host(
                ticket_type=TicketType.DAY_TICKET,
                meals=0,
                rule=Rule.PROGRAM_HELPER_1,
            )

        if program_involvements:
            return Perks.for_program_host(
                ticket_type=TicketType.DAY_TICKET,
                meals=0,
                rule=Rule.PROGRAM_NO_MATCH,
            )

        return Perks()

    @classmethod
    def get_dimension_dtos(cls, event: Event) -> list[DimensionDTO]:
        return [
            *super().get_dimension_dtos(event),
            TicketType.as_dimension_dto(),
            Rule.as_dimension_dto(),
        ]

    @classmethod
    def get_annotation_dtos(cls) -> list[AnnotationDTO]:
        perks = [
            AnnotationDTO(
                slug="tracon:mealVouchers",
                type=AnnotationDataType.NUMBER,
                title=dict(
                    en="Number of meal vouchers",
                    fi="Ruokalippujen määrä",
                ),
            ),
        ]

        for perk in perks:
            perk.is_applicable_to_program_items = False
            perk.is_applicable_to_schedule_items = False
            perk.is_applicable_to_involvements = True
            perk.is_perk = True

        return [*super().get_annotation_dtos(), *perks]

    def get_dimension_values(self) -> CachedDimensions:
        return {
            "v1-personnel-class": [self.perks.badge_type.v1_personnel_class_slug]
            if self.perks.badge_type.v1_personnel_class_slug
            else [],
            "ticket-type": [self.perks.ticket_type.value] if self.perks.ticket_type != TicketType.NONE else [],
            "perks-rule": [self.perks.rule.value] if self.perks.rule != Rule.NONE else [],
        }

    def get_annotation_values(self) -> dict[str, str | int | float | bool]:
        return {
            "internal:formattedPerks": self.perks.formatted_perks,
            "tracon:mealVouchers": self.perks.meals,
        }
