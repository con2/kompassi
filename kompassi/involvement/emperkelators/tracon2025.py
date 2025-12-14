"""
Tracon's rules for combining perks from multiple involvements.
Meal vouchers are granted based on working hours, stacking up to four.
Swag is granted based on working hours, with an extra swag item for working more than 14 hours.
"""

from __future__ import annotations

import logging
from enum import Enum
from functools import cached_property, reduce
from typing import Self

import pydantic

from kompassi.core.models.event import Event
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.cached_annotations import CachedAnnotations
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO
from kompassi.dimensions.models.enums import AnnotationDataType, ValueOrdering
from kompassi.forms.models.response import Response
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.graphql_api.utils import get_message_in_language
from kompassi.reports.graphql.report import Column, Report, TypeOfColumn

from ..models.enums import InvolvementType
from ..models.involvement import Involvement
from .base import BaseEmperkelator

logger = logging.getLogger(__name__)
THIRD_MEAL_MIN_HOURS = 12
FOURTH_MEAL_MIN_HOURS = 16
EXTRA_SWAG_MIN_HOURS = 14
MAX_MEALS = 4


class TicketType(Enum):
    NONE = "none", "Ei lippuetua", "No ticket"
    # MAY_BUY = "may-buy", "Voi ostaa lipun", "May buy a ticket"
    # DAY_TICKET = "day-ticket", "Päivälippu", "Day ticket"
    # WEEKEND_TICKET = "weekend-ticket", "Viikonloppulippu", "Weekend ticket"
    # EXTERNAL_BADGE = "external-badge", "Badge (external)", "Badge (external)"
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
                if tt != cls.NONE
            ],
            value_ordering=ValueOrdering.MANUAL,
        )

    def __lt__(self, other: TicketType) -> bool:
        return self.index < other.index


class ShirtSize(Enum):
    NONE = "none", "NO_SHIRT", "Nothing", "Ei työvoimatuotetta"
    UNISEX_XS = "unisex-xs", "XS", "XS Unisex", "XS Unisex"
    UNISEX_S = "unisex-s", "S", "S Unisex", "S Unisex"
    UNISEX_M = "unisex-m", "M", "M Unisex", "M Unisex"
    UNISEX_L = "unisex-l", "L", "L Unisex", "L Unisex"
    UNISEX_XL = "unisex-xl", "XL", "XL Unisex", "XL Unisex"
    UNISEX_2XL = "unisex-2xl", "XXL", "2XL Unisex", "2XL Unisex"
    UNISEX_3XL = "unisex-3xl", "3XL", "3XL Unisex", "3XL Unisex"
    UNISEX_4XL = "unisex-4xl", "4XL", "4XL Unisex", "4XL Unisex"
    UNISEX_5XL = "unisex-5xl", "5XL", "5XL Unisex", "5XL Unisex"
    LADYFIT_XS = "ladyfit-xs", "LF_XS", "XS Ladyfit", "XS Ladyfit"
    LADYFIT_S = "ladyfit-s", "LF_S", "S Ladyfit", "S Ladyfit"
    LADYFIT_M = "ladyfit-m", "LF_M", "M Ladyfit", "M Ladyfit"
    LADYFIT_L = "ladyfit-l", "LF_L", "L Ladyfit", "L Ladyfit"
    LADYFIT_XL = "ladyfit-xl", "LF_XL", "XL Ladyfit", "XL Ladyfit"
    LADYFIT_2XL = "ladyfit-2xl", "LF_XXL", "2XL Ladyfit", "2XL Ladyfit"
    LADYFIT_3XL = "ladyfit-3xl", "LF_3XL", "3XL Ladyfit", "3XL Ladyfit"
    BAG = "bag", "BAG", "Tote bag", "Kangaskassi"
    BOTTLE = "bottle", "BOTTLE", "Water bottle", "Juomapullo"

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
        if v2_shirt_size == "bag":
            return cls.BOTTLE

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


SHIRT_SIZES_BY_V1: dict[str, ShirtSize] = {ss.v1_slug: ss for ss in ShirtSize}

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
        extra_swag = " ja ekstrajuomapullo" if self.extra_swag else ""

        return f"{self.ticket_type.title_fi}, {meals}, {swag}{extra_swag}"

    @classmethod
    def for_legacy_signup(cls, involvement: Involvement) -> Perks:
        personnel_classes = set(involvement.cached_dimensions.get("v1-personnel-class", []))
        working_hours: int = involvement.annotations.get("kompassi:workingHours", 10)

        if "coniitti" in personnel_classes:
            return Perks(
                override_formatted_perks="Coniitin kirjekuori, valittu työvoimatuote, ekstrajuomapullo",
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
        return Perks(
            ticket_type=TicketType.INTERNAL_BADGE,
            meals=1,
            swag=True,
        )

    @classmethod
    def for_involvement(cls, involvement: Involvement) -> Perks:
        match involvement.type:
            case InvolvementType.LEGACY_SIGNUP:
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

    @cached_property
    def active_legacy_signup_involvement(self):
        return next(
            (
                involvement
                for involvement in self.involvements
                if involvement.type == InvolvementType.LEGACY_SIGNUP and involvement.is_active
            ),
            None,
        )

    @property
    def v1_personnel_class_dimension_values(self):
        if inv := self.active_legacy_signup_involvement:
            return inv.cached_dimensions.get("v1-personnel-class", [])

        for inv in self.involvements:
            if inv.type == InvolvementType.PROGRAM_HOST:
                return ["ohjelma"]

        return []

    @property
    def ticket_type_dimension_values(self) -> list[str]:
        return [self.perks.ticket_type.value] if self.perks.ticket_type != TicketType.NONE else []

    @property
    def shirt_size_dimension_values(self) -> list[str]:
        if inv := self.active_legacy_signup_involvement:
            return inv.cached_dimensions.get("shirt-size", [])

        # TODO in future events, make sure this is a dimension in source data
        for response in Response.objects.filter(
            form__survey__event=self.event,
            form__survey__slug__in=["program-swag", "programhost"],
            original_created_by=self.person.user,
        ):
            values, warnings = response.get_processed_form_data(field_slugs=["swag"])
            if "swag" in warnings:
                logger.warning(
                    "Cowardly refusing to emperkelate shirt size with warnings: %s",
                    dict(
                        person=self.person.id,
                        response=response.id,
                    ),
                )

            shirt_size_str = values.get("swag", "")
            if not shirt_size_str:
                continue

            try:
                shirt_size = ShirtSize.from_v2(shirt_size_str)
            except ValueError:
                logger.warning(
                    "Invalid shirt size value: %s",
                    dict(
                        person=self.person.id,
                        response=response.id,
                        shirt_size=shirt_size_str,
                    ),
                )
                continue

            return [shirt_size.value]

        return []

    @classmethod
    def get_dimension_dtos(cls, event: Event) -> list[DimensionDTO]:
        return [
            *super().get_dimension_dtos(event),
            TicketType.as_dimension_dto(),
            ShirtSize.as_dimension_dto(),
            PROGRAM_HOST_ROLE_DIMENSION_DTO,
        ]

    def get_dimension_values(self) -> CachedDimensions:
        return {
            "v1-personnel-class": self.v1_personnel_class_dimension_values,
            "ticket-type": self.ticket_type_dimension_values,
            "shirt-size": self.shirt_size_dimension_values,
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
            # Annotations are passed to Badge but dimensions are not.
            # So put formatted shirt size in an annotation.
            AnnotationDTO(
                slug="tracon:shirtSize",
                type=AnnotationDataType.STRING,
                title=dict(
                    en="Shirt size",
                    fi="T-paidan koko",
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
        annotations = self.perks.model_dump(
            mode="json",
            exclude_none=True,
            by_alias=True,
            exclude={"ticket_type"},
        )

        dimension_values = self.get_dimension_values()
        shirt_size_dvss = dimension_values.get("shirt-size", [])
        shirt_size = ShirtSize.from_v2(next(iter(shirt_size_dvss))) if shirt_size_dvss else ShirtSize.NONE
        annotations["tracon:shirtSize"] = shirt_size.title_fi

        return annotations

    def get_title(self) -> str:
        if inv := self.active_legacy_signup_involvement:
            return inv.title

        for involvement in self.involvements:
            if involvement.type == InvolvementType.PROGRAM_HOST:
                return "Ohjelmanpitäjä"

        return ""

    @classmethod
    def get_reports(cls, event: Event, lang: str = DEFAULT_LANGUAGE) -> list[Report]:
        """
        TODO Generalize this
        Use AnnotationFlags.PERK to filter and count all countable annotations (int or boolean)
        """
        annotation_dtos = cls.get_annotation_dtos()

        annotationsies = Involvement.objects.filter(
            universe=event.involvement_universe,
            type=InvolvementType.COMBINED_PERKS,
            is_active=True,
        ).values_list("annotations", flat=True)

        meal_vouchers_annotation_dto = next(dto for dto in annotation_dtos if dto.slug == "tracon:mealVouchers")
        meal_vouchers_title = get_message_in_language(meal_vouchers_annotation_dto.title, lang)
        total_meal_vouchers = sum(
            annotations.get("tracon:mealVouchers", 0) for annotations in annotationsies if isinstance(annotations, dict)
        )

        extra_swag_annotation_dto = next(dto for dto in annotation_dtos if dto.slug == "tracon:extraSwag")
        extra_swag_title = get_message_in_language(extra_swag_annotation_dto.title, lang)
        total_extra_swag = sum(
            annotations.get("tracon:extraSwag", False)
            for annotations in annotationsies
            if isinstance(annotations, dict)
        )

        return [
            *super().get_reports(event, lang),
            Report(
                slug="tracon2025_specific",
                title=dict(
                    fi="Tracon 2025: Muut edut",
                    en="Tracon 2025: Other perks",
                ),
                columns=[
                    Column(
                        slug="perk",
                        title=dict(
                            en="Perk",
                            fi="Etu",
                        ),
                        type=TypeOfColumn.STRING,
                    ),
                    Column(
                        slug="count",
                        title=dict(
                            en="Count",
                            fi="Lukumäärä",
                        ),
                        type=TypeOfColumn.INT,
                    ),
                ],
                rows=[
                    [extra_swag_title, total_extra_swag],
                    [meal_vouchers_title, total_meal_vouchers],
                ],
            ),
        ]
