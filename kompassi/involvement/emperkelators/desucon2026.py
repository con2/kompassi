from __future__ import annotations

import logging
from enum import Enum
from functools import cached_property, reduce

import pydantic

from kompassi.core.models.event import Event
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO
from kompassi.dimensions.models.enums import AnnotationDataType, ValueOrdering

from ..models.enums import InvolvementType
from ..models.involvement import Involvement
from .base import BaseEmperkelator

logger = logging.getLogger(__name__)


class TicketType(Enum):
    v1_personnel_class_slug: str | None
    title_fi: str
    title_en: str

    NONE = "none", None, "Ei lippua", "No ticket"
    CAN_BUY = "can-buy", None, "Saa ostaa lipun", "Can buy ticket"
    WEEKEND_TICKET = "weekend-ticket", None, "Viikonloppuranneke", "Weekend ticket"
    PERFORMER_BADGE = "performer-badge", "esiintyja", "Esiintyjäbadge", "Performer badge"
    PROGRAM_BADGE = "program-badge", "ohjelma", "Ohjelmabadge", "Program host badge"
    VOLUNTEER_BADGE = "volunteer-badge", "tyovoima", "Työvoimabadge", "Volunteer badge"
    OVERSEER_BADGE = "overseer-badge", "vuorovastaava", "Ylikuuttibadge", "Overseer badge"
    ORGANIZER_BADGE = "organizer-badge", "vastaava", "Vastaavabadge", "Organizer badge"

    def __new__(cls, value: str, v1_personnel_class_slug: str | None, title_fi: str, title_en: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.v1_personnel_class_slug = v1_personnel_class_slug
        obj.title_fi = title_fi
        obj.title_en = title_en
        return obj

    def __lt__(self, other: TicketType) -> bool:
        return TICKET_TYPES.index(self) < TICKET_TYPES.index(other)

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


# for use only by __lt__, others should iterate over TicketType
TICKET_TYPES = list(TicketType)


class ShirtType(Enum):
    v1_slug: str
    title_fi: str
    title_en: str

    NONE = "none", "NO_SHIRT", "Ei paitaa", "No shirt"
    STAFF = "staff", "STAFF", "STAFF-paita", "STAFF shirt"
    DESUTV = "desutv", "DESUTV", "DESUTV-paita", "DESUTV shirt"
    KUVAAJA = "kuvaaja", "KUVAAJA", "KUVAAJA-paita", "KUVAAJA shirt"
    DESURITY = "desurity", "DESURITY", "DESURITY-paita", "DESURITY shirt"

    def __new__(cls, value: str, v1_slug: str, title_fi: str, title_en: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.v1_slug = v1_slug
        obj.title_en = title_en
        obj.title_fi = title_fi

        return obj

    @classmethod
    def from_v1(cls, v1_shirt_size: str) -> ShirtType:
        return SHIRT_TYPES_BY_V1.get(v1_shirt_size, cls.NONE)

    @classmethod
    def from_v2(cls, v2_shirt_size: str) -> ShirtType:
        return cls(v2_shirt_size)

    @classmethod
    def as_dimension_dto(cls) -> DimensionDTO:
        return DimensionDTO(
            slug="shirt-type",
            title=dict(
                en="Shirt type",
                fi="Paitatyyppi",
            ),
            choices=[
                DimensionValueDTO(
                    slug=tt.value,
                    title=dict(
                        fi=tt.title_fi,
                        en=tt.title_en,
                    ),
                )
                for tt in cls
            ],
            is_list_filter=False,
            is_shown_in_detail=True,
            value_ordering=ValueOrdering.MANUAL,
        )

    def __lt__(self, other: ShirtType) -> bool:
        return SHIRT_TYPES.index(self) < SHIRT_TYPES.index(other)

    def combine(self, other: ShirtType) -> ShirtType:
        return max(self, other)


SHIRT_TYPES_BY_V1: dict[str, ShirtType] = {st.v1_slug: st for st in ShirtType}
SHIRT_TYPES = list(ShirtType)  # for use only by __lt__, others should iterate over ShirtType


class ShirtSize(Enum):
    NONE = "none", "NO_SHIRT", "No shirt", "Ei paitaa"
    UNISEX_XS = "xs-unisex", "XS", "XS Unisex", "XS Unisex"
    UNISEX_S = "s-unisex", "S", "S Unisex", "S Unisex"
    UNISEX_M = "m-unisex", "M", "M Unisex", "M Unisex"
    UNISEX_L = "l-unisex", "L", "L Unisex", "L Unisex"
    UNISEX_XL = "xl-unisex", "XL", "XL Unisex", "XL Unisex"
    UNISEX_2XL = "2xl-unisex", "XXL", "2XL Unisex", "2XL Unisex"
    UNISEX_3XL = "3xl-unisex", "3XL", "3XL Unisex", "3XL Unisex"
    UNISEX_4XL = "4xl-unisex", "4XL", "4XL Unisex", "4XL Unisex"
    UNISEX_5XL = "5xl-unisex", "5XL", "5XL Unisex", "5XL Unisex"
    LADYFIT_XS = "xs-ladyfit", "LF_XS", "XS Ladyfit", "XS Ladyfit"
    LADYFIT_S = "s-ladyfit", "LF_S", "S Ladyfit", "S Ladyfit"
    LADYFIT_M = "m-ladyfit", "LF_M", "M Ladyfit", "M Ladyfit"
    LADYFIT_L = "l-ladyfit", "LF_L", "L Ladyfit", "L Ladyfit"
    LADYFIT_XL = "xl-ladyfit", "LF_XL", "XL Ladyfit", "XL Ladyfit"

    v1_slug: str
    title_fi: str
    title_en: str

    def __new__(cls, value: str, v1_slug: str, title_en: str, title_fi: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.v1_slug = v1_slug
        obj.title_en = title_en
        obj.title_fi = title_fi

        return obj

    @classmethod
    def from_v1(cls, v1_shirt_size: str) -> ShirtSize:
        return SHIRT_SIZES_BY_V1.get(v1_shirt_size, cls.NONE)

    @classmethod
    def from_v2(cls, v2_shirt_size: str) -> ShirtSize:
        match v2_shirt_size:
            case "no-shirt":
                return cls.NONE
            case "xxl-unisex":
                return cls.UNISEX_2XL
            case _:
                return cls(v2_shirt_size)

    @classmethod
    def as_dimension_dto(cls) -> DimensionDTO:
        return DimensionDTO(
            slug="shirt-size",
            title=dict(
                en="Shirt size",
                fi="Paitakoko",
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
            is_list_filter=False,
            is_shown_in_detail=True,
            value_ordering=ValueOrdering.MANUAL,
        )

    def combine(self, other: ShirtSize) -> ShirtSize:
        return other if other != ShirtSize.NONE else self


SHIRT_SIZES_BY_V1: dict[str, ShirtSize] = {ss.v1_slug: ss for ss in ShirtSize}


class Perks(pydantic.BaseModel):
    ticket_type: TicketType = TicketType.NONE
    shirt_type: ShirtType = ShirtType.NONE
    shirt_size: ShirtSize = ShirtSize.NONE
    meals: int = 0
    override_formatted_perks: str = ""

    @property
    def formatted_perks(self) -> str:
        if self.override_formatted_perks:
            return self.override_formatted_perks

        parts = []

        if self.shirt_type == ShirtType.NONE or self.shirt_size == ShirtSize.NONE:
            parts.append("Ei paitaa")
        else:
            parts.append(f"{self.shirt_type.title_fi} ({self.shirt_size.title_fi})")

        if self.meals == 1:
            parts.append("1 ruokalippu")
        elif self.meals > 1:
            parts.append(f"{self.meals} ruokalippua")

        return ", ".join(parts)

    @classmethod
    def for_legacy_signup(cls, involvement: Involvement) -> Perks:
        signup = involvement.signup
        signup_extra = signup.signup_extra if signup else None
        if signup is None or signup_extra is None:
            logger.warning("Legacy signup involvement %d has no signup_extra", involvement.id)
            return Perks()

        shirt_size = ShirtSize.from_v1(signup_extra.shirt_size)
        personnel_classes = [pc.slug for pc in signup.personnel_classes.all()]
        job_categories = [jc.slug for jc in signup.job_categories_accepted.all()]
        job_title_lower = (signup.job_title or "").lower()

        if "jarjestyksenvalvoja" in job_categories or "jv" in job_categories or "turvallisuus" in job_title_lower:
            shirt_type = ShirtType.DESURITY
        elif "valokuvaaja" in job_categories or "valokuvaus" in job_categories or "valokuvaus" in job_title_lower:
            shirt_type = ShirtType.KUVAAJA
        elif "desutv" in job_categories or "desutv" in job_title_lower:
            shirt_type = ShirtType.DESUTV
        else:
            shirt_type = ShirtType.STAFF

        meals = 2
        ticket_type = TicketType.VOLUNTEER_BADGE

        if "vastaava" in personnel_classes:
            ticket_type = TicketType.ORGANIZER_BADGE
            meals = 3
        elif "ylikuutti" in personnel_classes or "vuorovastaava" in personnel_classes:
            ticket_type = TicketType.OVERSEER_BADGE

        return Perks(
            ticket_type=ticket_type,
            shirt_type=shirt_type,
            shirt_size=shirt_size,
            meals=meals,
            override_formatted_perks=signup.override_formatted_perks,
        )

    @classmethod
    def for_program_host(cls, involvement: Involvement) -> Perks:
        response = involvement.response
        if response is None:
            logger.warning("Program host %d has no response", involvement.id)
            return Perks()

        values, warnings = response.get_processed_form_data(field_slugs=["shirt_size"])
        if "shirt-size" in warnings:
            logger.warning(
                "Cowardly refusing to emperkelate shirt size with warnings: %s",
                dict(
                    involvement=involvement.id,
                    response=response.id,
                ),
            )
            shirt_size = ShirtSize.NONE
        else:
            shirt_size_value = values.get("shirt_size")
            shirt_size = ShirtSize.from_v2(shirt_size_value) if isinstance(shirt_size_value, str) else ShirtSize.NONE

        perks = Perks(
            shirt_size=shirt_size,
            shirt_type=ShirtType.STAFF,
        )

        program_host_type_values = involvement.cached_dimensions.get("program-host-type", [])
        for program_host_type_value in program_host_type_values:
            match program_host_type_value:
                case "talk-program":
                    perks.imbibe(
                        Perks(
                            ticket_type=TicketType.PROGRAM_BADGE,
                            meals=2,
                        )
                    )
                case "performance":
                    perks.imbibe(
                        Perks(
                            ticket_type=TicketType.PERFORMER_BADGE,
                            meals=1,
                        )
                    )
                case _:
                    perks.imbibe(
                        Perks(
                            ticket_type=TicketType.PROGRAM_BADGE,
                            meals=1,
                        )
                    )

        return perks

    @classmethod
    def for_involvement(cls, involvement: Involvement) -> Perks:
        match involvement.type:
            case InvolvementType.LEGACY_SIGNUP:
                return Perks.for_legacy_signup(involvement)

            case InvolvementType.PROGRAM_HOST:
                return Perks.for_program_host(involvement)

        return Perks()

    def imbibe(self, perks: Perks):
        self.ticket_type = self.ticket_type.combine(perks.ticket_type)
        self.shirt_type = self.shirt_type.combine(perks.shirt_type)
        self.shirt_size = self.shirt_size.combine(perks.shirt_size)

        # Currently the meal vouchers do not stack. This may change in the future (NOTE: define upper limit).
        self.meals = max(self.meals, perks.meals)

        self.override_formatted_perks = perks.override_formatted_perks or self.override_formatted_perks or ""
        return self


PROGRAM_HOST_TYPE_DIMENSION_DTO = DimensionDTO(
    slug="program-host-type",
    title=dict(
        en="Program host type",
        fi="Ohjelmanpitäjäluokka",
    ),
    choices=[],  # Saved using remove_other_values=False
)


class DesuconEmperkelator(BaseEmperkelator):
    @cached_property
    def perks(self) -> Perks:
        return reduce(
            Perks.imbibe,
            (Perks.for_involvement(inv) for inv in self.involvements),
            Perks(),
        )

    @classmethod
    def get_dimension_dtos(cls, event: Event) -> list[DimensionDTO]:
        return [
            *super().get_dimension_dtos(event),
            TicketType.as_dimension_dto(),
            ShirtType.as_dimension_dto(),
            ShirtSize.as_dimension_dto(),
            PROGRAM_HOST_TYPE_DIMENSION_DTO,
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
            "v1-personnel-class": [self.perks.ticket_type.v1_personnel_class_slug]
            if self.perks.ticket_type.v1_personnel_class_slug
            else [],
            "ticket-type": [self.perks.ticket_type.value] if self.perks.ticket_type != TicketType.NONE else [],
            "shirt-type": [self.perks.shirt_type.value] if self.perks.ticket_type != TicketType.NONE else [],
            "shirt-size": [self.perks.shirt_size.value] if self.perks.ticket_type != TicketType.NONE else [],
        }

    def get_annotation_values(self) -> dict[str, str | int | float | bool]:
        return {
            "internal:formattedPerks": self.perks.formatted_perks,
            "tracon:mealVouchers": self.perks.meals,
        }
