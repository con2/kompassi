from __future__ import annotations

from datetime import date
from enum import Enum
from functools import cached_property

from kompassi.core.models.event import Event
from kompassi.dimensions.models.cached_annotations import CachedAnnotations
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.dimensions.models.dimension_dto import DimensionDTO
from kompassi.dimensions.models.dimension_value_dto import DimensionValueDTO
from kompassi.dimensions.models.enums import ValueOrdering
from kompassi.involvement.emperkelators.base import BaseEmperkelator
from kompassi.involvement.models.enums import InvolvementType
from kompassi.involvement.models.involvement import Involvement

SATURDAY = 5
SUNDAY = 6

# V1 personnel classes that always get a weekend ticket
WEEKEND_TICKET_PERSONNEL_CLASSES = {"vastaava", "vapaaehtoinen"}

# Seller personnel classes and the weekdays they grant tickets for
SELLER_PERSONNEL_CLASS_WEEKDAYS = {
    "myyja-la": {SATURDAY},
    "myyja-su": {SUNDAY},
    "myyja-vkl": {SATURDAY, SUNDAY},
}


class TicketType(Enum):
    """
    Volunteers (vastaava, vapaaehtoinen) always get a weekend ticket.
    Program hosts get a day ticket for the day(s) their program is scheduled on,
    or a weekend ticket if they have program on both days.
    """

    title_fi: str
    title_en: str

    NONE = "none", "Ei lippuetua", "No ticket benefit"
    DAY_TICKET_SATURDAY = "day-ticket-saturday", "Päivälippu lauantai", "Day ticket Saturday"
    DAY_TICKET_SUNDAY = "day-ticket-sunday", "Päivälippu sunnuntai", "Day ticket Sunday"
    WEEKEND_TICKET = "weekend-ticket", "Viikonloppulippu", "Weekend ticket"

    def __new__(cls, value: str, title_fi: str, title_en: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title_fi = title_fi
        obj.title_en = title_en
        return obj

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

    @classmethod
    def from_weekdays(cls, weekdays: set[int]) -> TicketType:
        if not weekdays:
            return cls.NONE
        if weekdays == {SATURDAY}:
            return cls.DAY_TICKET_SATURDAY
        if weekdays == {SUNDAY}:
            return cls.DAY_TICKET_SUNDAY
        return cls.WEEKEND_TICKET


class KotaeEmperkelator(BaseEmperkelator):
    @cached_property
    def has_varakettu_signup(self) -> bool:
        return any(
            involvement.type == InvolvementType.LEGACY_SIGNUP and involvement.title.casefold() == "varakettu"
            for involvement in self.involvements
        )

    def _get_program_weekdays(self, involvement: Involvement) -> set[int]:
        if not involvement.program:
            return set()

        tz = self.event.timezone
        return {
            date.fromisoformat(date_str).weekday()
            for schedule_item in involvement.program.schedule_items.all()
            for date_str in schedule_item.get_date_dimension_value(tz=tz)
        }

    @cached_property
    def ticket_type(self) -> TicketType:
        if self.has_varakettu_signup:
            return TicketType.NONE

        for involvement in self.involvements:
            if involvement.type != InvolvementType.LEGACY_SIGNUP or involvement.signup is None:
                continue

            personnel_classes = set(involvement.signup.personnel_classes.values_list("slug", flat=True))
            if personnel_classes & WEEKEND_TICKET_PERSONNEL_CLASSES:
                return TicketType.WEEKEND_TICKET

            seller_weekdays: set[int] = set()
            for slug in personnel_classes & SELLER_PERSONNEL_CLASS_WEEKDAYS.keys():
                seller_weekdays |= SELLER_PERSONNEL_CLASS_WEEKDAYS[slug]
            if seller_weekdays:
                return TicketType.from_weekdays(seller_weekdays)

        weekdays: set[int] = set()
        for involvement in self.involvements:
            if involvement.type == InvolvementType.PROGRAM_HOST:
                weekdays |= self._get_program_weekdays(involvement)

        return TicketType.from_weekdays(weekdays)

    @classmethod
    def get_dimension_dtos(cls, event: Event) -> list[DimensionDTO]:
        return [
            *super().get_dimension_dtos(event),
            TicketType.as_dimension_dto(),
        ]

    def get_dimension_values(self) -> CachedDimensions:
        return {
            "ticket-type": [self.ticket_type.value] if self.ticket_type != TicketType.NONE else [],
        }

    def get_annotation_values(self) -> CachedAnnotations:
        if self.has_varakettu_signup:
            return {"internal:overrideFormattedPerks": "ÄLÄ ANNA BADGEA"}

        return super().get_annotation_values()

    @classmethod
    def _format_computed_perks(cls, dimension_values: CachedDimensions, annotation_values: CachedAnnotations) -> str:
        ticket_type_values = dimension_values.get("ticket-type", [])
        ticket_type = TicketType(next(iter(ticket_type_values))) if ticket_type_values else TicketType.NONE

        if ticket_type == TicketType.NONE:
            return ""

        return ticket_type.title_fi
