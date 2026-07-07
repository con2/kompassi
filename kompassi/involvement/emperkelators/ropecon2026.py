from __future__ import annotations

import logging
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


class Perks(pydantic.BaseModel):
    badge_type: BadgeType = BadgeType.NONE
    ticket_type: TicketType = TicketType.NONE
    meals: int = 0
    override_formatted_perks: str = ""

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
    def for_legacy_signup(cls, involvement: Involvement) -> Perks:
        if involvement.type != InvolvementType.LEGACY_SIGNUP:
            raise ValueError(f"Expected involvement type {InvolvementType.LEGACY_SIGNUP}, got {involvement.type}")
        if involvement.signup is None:
            raise ValueError("Expected involvement to have a signup, but it was None")

        personnel_classes = set(involvement.signup.personnel_classes.values_list("slug", flat=True))
        if "conitea" in personnel_classes:
            ticket_type = TicketType.WEEKEND_TICKET
            badge_type = BadgeType.ORGANIZER_BADGE
            meals = 2
        elif "tyovoima" in personnel_classes or "ylivankari" in personnel_classes or "ylityovoima" in personnel_classes:
            ticket_type = TicketType.WEEKEND_TICKET
            badge_type = BadgeType.VOLUNTEER_BADGE
            meals = 2
        else:
            ticket_type = TicketType.NONE
            badge_type = BadgeType.NONE
            meals = 0

        return Perks(
            ticket_type=ticket_type,
            badge_type=badge_type,
            meals=meals,
            override_formatted_perks=involvement.signup.override_formatted_perks,
        )

    @classmethod
    def for_program_host(cls, ticket_type: TicketType, meals: int) -> Perks:
        return Perks(
            badge_type=BadgeType.PROGRAM_BADGE,
            ticket_type=ticket_type,
            meals=meals,
        )


class RopeconEmperkelator(BaseEmperkelator):
    @cached_property
    def perks(self) -> Perks:
        if (
            v1_signup := next((i for i in self.involvements if i.type == InvolvementType.LEGACY_SIGNUP), None)
        ) is not None:
            return Perks.for_legacy_signup(v1_signup)

        program_involvements = [i for i in self.involvements if i.type == InvolvementType.PROGRAM_HOST]
        main_involvements = [
            i for i in program_involvements if i.response and i.response.survey.slug != "offer-program-hosts"
        ]
        main_program_host_involvements_over6h = [i for i in main_involvements if i.program and i.program]
        helper_involvements = [
            i for i in program_involvements if i.response and i.response.survey.slug == "offer-program-hosts"
        ]

        # päävastuullinen vähintään 2 aikataulumerkinnässä TAI
        # päävastuullinen yhdessä aikataulumerkinnässä, joka kestää 6 h tai enemmän TAI
        # päävastuullinen yhdessä aikataulumerkinnässä ja ohjelma-apuri jossain muussa ohjelmassa -> viikonloppulippu + 1 ruokalippu
        if (
            len(main_involvements) >= 2
            or len(main_program_host_involvements_over6h) > 0
            or (len(main_involvements) == 1 and len(helper_involvements) > 0)
        ):
            return Perks.for_program_host(ticket_type=TicketType.WEEKEND_TICKET, meals=1)

        # päävastuullinen yhdessä aikataulumerkinnässä -> päivälippu + 1 ruokalippu
        if len(main_involvements) == 1:
            return Perks.for_program_host(ticket_type=TicketType.DAY_TICKET, meals=1)

        # ohjelma-apuri vähintään 2 aikataulumerkinnässä -> viikonloppulippu (ei ruokaa)
        if len(helper_involvements) >= 2:
            return Perks.for_program_host(ticket_type=TicketType.WEEKEND_TICKET, meals=0)

        # ohjelma-apuri yhdessä aikataulumerkinnässä -> päivälippu (ei ruokaa)
        if len(helper_involvements) == 1:
            return Perks.for_program_host(ticket_type=TicketType.DAY_TICKET, meals=0)

        if program_involvements:
            raise ValueError(
                f"Unexpected program involvements that do not match any perk rules for person {self.person.id}: {program_involvements}"
            )

        return Perks()

    @classmethod
    def get_dimension_dtos(cls, event: Event) -> list[DimensionDTO]:
        return [
            *super().get_dimension_dtos(event),
            TicketType.as_dimension_dto(),
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
        }

    def get_annotation_values(self) -> dict[str, str | int | float | bool]:
        return {
            "internal:formattedPerks": self.perks.formatted_perks,
            "tracon:mealVouchers": self.perks.meals,
        }
