import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from django.utils.timezone import get_current_timezone

from core.models import Event
from programme.models.category import Category
from programme.models.programme import Programme

from ..consts import (
    CATEGORY_DIMENSION_TITLE_LOCALIZED,
    DATE_DIMENSION_TITLE_LOCALIZED,
    DEFAULT_COLORS,
    ROOM_DIMENSION_TITLE_LOCALIZED,
)
from ..integrations.konsti import KONSTI_DIMENSION_DTO
from ..models.dimension import DimensionDTO, DimensionValueDTO, ValueOrdering
from .default import DefaultImporter

logger = logging.getLogger("kompassi")
tz = get_current_timezone()


@dataclass
class TraconImporter(DefaultImporter):
    event: Event
    language: str = "fi"

    date_cutoff_time = timedelta(hours=4)  # 04:00 local time

    def get_dimensions(self) -> list[DimensionDTO]:
        return [
            DimensionDTO(
                slug="date",
                title=DATE_DIMENSION_TITLE_LOCALIZED,
                choices=list(self._get_date_dimension_values()),
                value_ordering=ValueOrdering.SLUG,
            ),
            DimensionDTO(
                slug="category",
                title=CATEGORY_DIMENSION_TITLE_LOCALIZED,
                choices=[
                    DimensionValueDTO(
                        slug=category.slug,
                        title={self.language: category.title},
                        color=DEFAULT_COLORS.get(category.style, ""),
                    )
                    for category in Category.objects.filter(event=self.event, public=True)
                ],
            ),
            # no tag dimension!
            DimensionDTO(
                slug="accessibility",
                is_negative_selection=True,
                title=dict(
                    fi="Esteettömyys",
                    en="Accessibility",
                    sv="Tillgänglighet",
                ),
                value_ordering=ValueOrdering.TITLE,
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                        ),
                    )
                    for slug, title_fi, title_en in [
                        ("flashing-lights", "Kirkkaita/välkkyviä valoja", "Bright/flashing lights"),
                        ("loud-noises", "Kovia ääniä", "Loud noises"),
                        ("smoke-effects", "Savutehosteita", "Smoke effects"),
                    ]
                ],
            ),
            DimensionDTO(
                slug="audience",
                title=dict(
                    fi="Kohderyhmä",
                    en="Target Audience",
                    sv="Målgrupp",
                ),
                value_ordering=ValueOrdering.MANUAL,
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                        ),
                    )
                    for slug, title_fi, title_en, title_sv in [
                        ("unrestricted", "Ei ikärajaa", "No age limit", "Ingen åldersgräns"),
                        ("r18", "K-18", "For ages 18 and up", "För personer över 18 år"),
                        ("child-friendly", "Lapsiystävällinen", "Child-friendly", "Barnvänlig"),
                        ("beginner-friendly", "Aloittelijaystävällinen", "Beginner-friendly", "Nybörjarvänlig"),
                        ("experienced", "Kokeneille", "For experienced", "För erfarna"),
                    ]
                ],
            ),
            DimensionDTO(
                slug="language",
                title=dict(fi="Kieli", en="Language", sv="Språk"),
                value_ordering=ValueOrdering.MANUAL,
                # TODO make visible when populated
                is_shown_in_detail=False,
                is_list_filter=False,
                choices=[
                    DimensionValueDTO(slug="fi", title=dict(fi="Suomi", en="Finnish", sv="Finska")),
                    DimensionValueDTO(slug="en", title=dict(fi="Englanti", en="English", sv="Engelska")),
                    DimensionValueDTO(slug="free", title=dict(fi="Kielivapaa", en="Language free", sv="Språkfri")),
                ],
            ),
            DimensionDTO(
                slug="room",
                title=ROOM_DIMENSION_TITLE_LOCALIZED,
                choices=list(self._get_room_dimension_values()),
            ),
            DimensionDTO(
                slug="signup",
                title=dict(
                    fi="Ennakkoilmoittautuminen",
                    en="Advance Registration",
                    sv="Förhandsanmälan",
                ),
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                        ),
                    )
                    for slug, title_fi, title_en, title_sv in [
                        ("none", "Ei ennakkoilmoittautumista", "No advance registration", "Ingen förhandsanmälan"),
                        ("tickets", "Erilliset pääsyliput", "Separate tickets", "Separata biljetter"),
                        ("paikkala", "Maksuttomat paikkaliput", "Free seating tickets", "Gratis sittplatsbiljetter"),
                        ("konsti", "Ilmoittautuminen Konstilla", "Registration via Konsti", "Anmälan via Konsti"),
                        ("form", "Ilmoittautuminen lomakkeella", "Registration via form", "Anmälan via formulär"),
                    ]
                ],
            ),
            KONSTI_DIMENSION_DTO,
        ]

    def get_program_dimension_values(self, programme: Programme) -> dict[str, list[str]]:
        dimensions = super().get_program_dimension_values(programme)

        audience = dimensions.setdefault("audience", [])
        if programme.is_age_restricted:
            audience.append("r18")
        if programme.is_children_friendly:
            audience.append("child-friendly")
        if programme.is_beginner_friendly:
            audience.append("beginner-friendly")
        if programme.is_intended_for_experienced_participants:
            audience.append("experienced")
        if "r18" not in audience:
            audience.append("unrestricted")

        signup = dimensions.setdefault("signup", [])
        if link := programme.signup_link:
            if "forms" in link or "survey" in link:
                signup.append("form")
            if "konsti" in link:
                signup.append("konsti")
            if "lippu.fi" in link:
                signup.append("tickets")
        if programme.is_using_paikkala:
            signup.append("paikkala")
        if not signup:
            signup.append("none")

        return dimensions

    def get_program_annotations(self, programme: Programme) -> dict[str, Any]:
        annotations = super().get_program_annotations(programme)
        dimension_values = self.get_program_dimension_values(programme)

        is_konsti = len(dimension_values.get("konsti", [])) > 0
        if is_konsti:
            annotations["internal:links:signup"] = f"https://ropekonsti.fi/program/item/{programme.slug}"

        if "lippu.fi" in programme.signup_link:
            annotations["internal:links:tickets"] = programme.signup_link
            annotations["internal:links:signup"] = ""

        if "paikkala" in dimension_values.get("signup", []):
            annotations["internal:links:reservation"] = "https://kompassi.eu/profile/reservations"

        return annotations
