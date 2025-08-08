"""
Tracon's rules for combining perks from multiple involvements.
Meal vouchers are granted based on working hours, stacking up to four.
Swag is granted based on working hours, with an extra swag item for working more than 14 hours.
"""

from __future__ import annotations

from enum import Enum
from functools import cached_property, reduce
from typing import TYPE_CHECKING, Self

import pydantic

from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.cached_annotations import CachedAnnotations
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO
from kompassi.dimensions.models.enums import AnnotationDataType

from ..models.enums import InvolvementType
from .base import BaseEmperkelator

if TYPE_CHECKING:
    from ..models.involvement import Involvement


THIRD_MEAL_MIN_HOURS = 12
FOURTH_MEAL_MIN_HOURS = 16
EXTRA_SWAG_MIN_HOURS = 14
MAX_MEALS = 4


class TicketType(Enum):
    NONE = "none", "Ei lippuetua", "No ticket"
    MAY_BUY = "may-buy", "Voi ostaa lipun", "May buy a ticket"
    DAY_TICKET = "day-ticket", "Päivälippu", "Day ticket"
    WEEKEND_TICKET = "weekend-ticket", "Viikonloppulippu", "Weekend ticket"
    EXTERNAL_BADGE = "external-badge", "Badge (external)", "Badge (external)"
    INTERNAL_BADGE = "internal-badge", "Badge (internal)", "Badge (internal)"
    SUPER_INTERNAL_BADGE = "super-internal-badge", "Badge (super internal)", "Badge (super internal)"

    title_fi: str
    title_en: str

    def __new__(cls, value: str, title: str, title_en: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title_fi = title
        obj.title_en = title_en
        return obj

    @cached_property
    def index(self) -> int:
        return list(TicketType).index(self)

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
            ],
        )

    def __lt__(self, other: TicketType) -> bool:
        return self.index < other.index


PROGRAM_HOST_ROLE_DIMENSION_DTO = DimensionDTO(
    slug="program-host-role",
    title=dict(
        en="Program host role",
        fi="Ohjelmanpitäjän rooli",
    ),
    choices=[
        DimensionValueDTO(
            slug="program-organizer",
            title=dict(
                en="Program organizer",
                fi="Ohjelmanjärjestäjä",
            ),
        ),
        DimensionValueDTO(
            slug="performer",
            title=dict(
                en="Performer",
                fi="Esiintyjä",
            ),
        ),
        DimensionValueDTO(
            slug="discussion-host",
            title=dict(
                en="Discussion host",
                fi="Keskustelupiirin vetäjä",
            ),
        ),
        DimensionValueDTO(
            slug="workshop-host",
            title=dict(
                en="Workshop host",
                fi="Työpajanpitäjä",
            ),
        ),
    ],
)


class Perks(pydantic.BaseModel):
    ticket_type: TicketType = pydantic.Field(default=TicketType.NONE, serialization_alias="ticket-type")
    meals: int = pydantic.Field(default=0, serialization_alias="tracon:mealVouchers")
    swag: bool = pydantic.Field(default=False, serialization_alias="tracon:swag")
    extra_swag: bool = pydantic.Field(default=False, serialization_alias="tracon:extraSwag")
    override_formatted_perks: str = pydantic.Field(default="", serialization_alias="internal:overrideFormattedPerks")

    @pydantic.computed_field(alias="internal:formattedPerks")
    def formatted_perks(self) -> str:
        if self.override_formatted_perks:
            return self.override_formatted_perks

        meals = f"{self.meals} ruokalippua" if self.meals else "ei ruokalippuja"
        swag = "valittu työvoimatuote" if self.swag else "ei työvoimatuotteita"
        extra_swag = " ja ekstrakangaskassi" if self.extra_swag else ""

        return f"{self.ticket_type.title_fi}, {meals}, {swag}{extra_swag}"

    @classmethod
    def for_legacy_signup(cls, involvement: Involvement) -> Perks:
        personnel_classes = set(involvement.cached_dimensions.get("v1-personnel-class", []))
        working_hours: int = involvement.annotations.get("kompassi:workingHours", 10)

        if "coniitti" in personnel_classes:
            return Perks(
                override_formatted_perks="Coniitin kirjekuori, valittu työvoimatuote, ekstrakangaskassi",
                ticket_type=TicketType.SUPER_INTERNAL_BADGE,
                meals=MAX_MEALS,
                swag=True,
                extra_swag=True,
            )
        elif "duniitti" in personnel_classes or "vuorovastaava" in personnel_classes:
            perks = Perks(
                ticket_type=TicketType.SUPER_INTERNAL_BADGE,
                meals=2,
                swag=True,
            )
        elif "tyovoima" in personnel_classes:
            perks = Perks(
                ticket_type=TicketType.INTERNAL_BADGE,
                meals=2,
                swag=True,
            )
        else:
            return Perks()

        # Grant extra perks based on working hours
        extra_meal_voucher = Perks(meals=1)
        extra_swag = Perks(extra_swag=True)
        if working_hours >= THIRD_MEAL_MIN_HOURS:
            perks.imbibe(extra_meal_voucher)
        if working_hours >= FOURTH_MEAL_MIN_HOURS:
            perks.imbibe(extra_meal_voucher)
        if working_hours >= EXTRA_SWAG_MIN_HOURS:
            perks.imbibe(extra_swag)

        return perks

    @classmethod
    def for_program_host(cls, involvement: Involvement) -> Perks:
        match involvement.cached_dimensions.get("program-host-role", ""):
            case "program-organizer":
                return Perks(
                    ticket_type=TicketType.INTERNAL_BADGE,
                    meals=1,
                    swag=True,
                )
            case "performer":
                return Perks(
                    ticket_type=TicketType.INTERNAL_BADGE,
                    meals=1,
                    swag=True,
                )
            case "discussion-host":
                return Perks(
                    ticket_type=TicketType.INTERNAL_BADGE,
                    meals=1,
                    swag=False,
                )
            case "workshop-host":
                return Perks(
                    ticket_type=TicketType.INTERNAL_BADGE,
                    meals=1,
                    swag=False,
                )
            case _:
                return Perks()

    @classmethod
    def for_involvement(cls, involvement: Involvement) -> Perks:
        match involvement.type:
            case InvolvementType.LEGACY_SIGNUP if involvement.signup:
                return Perks.for_legacy_signup(involvement)

            case InvolvementType.PROGRAM_HOST:
                return Perks.for_program_host(involvement)

        return Perks()

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


class TraconEmperkelator(BaseEmperkelator):
    @cached_property
    def perks(self) -> Perks:
        return reduce(Perks.imbibe, (Perks.for_involvement(inv) for inv in self.involvements), Perks())

    @classmethod
    def get_dimension_dtos(cls) -> list[DimensionDTO]:
        return [
            TicketType.as_dimension_dto(),
            PROGRAM_HOST_ROLE_DIMENSION_DTO,
        ]

    def get_dimension_values(self) -> CachedDimensions:
        return {
            "ticket-type": [self.perks.ticket_type.value],
        }

    @classmethod
    def get_annotation_dtos(cls) -> list[AnnotationDTO]:
        perks = [
            AnnotationDTO(
                slug="tracon:swag",
                type=AnnotationDataType.BOOLEAN,
                title=dict(
                    en="Swag included",
                    fi="Saa työvoimatuotteen",
                ),
            ),
            AnnotationDTO(
                slug="tracon:extraSwag",
                type=AnnotationDataType.BOOLEAN,
                title=dict(
                    en="Extra swag included",
                    fi="Saa ylimääräisen työvoimatuotteen",
                ),
            ),
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

    def get_annotation_values(self) -> CachedAnnotations:
        return self.perks.model_dump(mode="json", exclude_none=True, by_alias=True, exclude={"ticket_type"})

    def get_title(self) -> str:
        if signup := next((involvement.signup for involvement in self.involvements if involvement.signup), None):
            return signup.some_job_title

        if program_hostage := next(
            (involvement for involvement in self.involvements if involvement.type == InvolvementType.PROGRAM_HOST), None
        ):
            role_idv = program_hostage.dimensions.filter(value__dimension__slug="program-host-role").first()
            if role_idv:
                return role_idv.value.title_fi

        return ""
