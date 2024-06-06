from __future__ import annotations

import logging
from dataclasses import dataclass

from django.utils.timezone import get_current_timezone

from core.models import Event
from programme.models.programme import Programme
from programme.models.room import Room

from ..consts import DATE_DIMENSION_TITLE_LOCALIZED, ROOM_DIMENSION_TITLE_LOCALIZED
from ..models.dimension import DimensionDTO, DimensionValueDTO
from .default import DefaultImporter

logger = logging.getLogger("kompassi")
tz = get_current_timezone()


@dataclass
class RopeconImporter(DefaultImporter):
    event: Event
    language: str = "fi"

    def get_dimensions(self):
        return [
            DimensionDTO(
                slug="date",
                title=DATE_DIMENSION_TITLE_LOCALIZED,
                choices=list(self._get_date_dimension_values()),
            ),
            DimensionDTO(
                slug="type",
                title=dict(
                    fi="Ohjelmatyyppi",
                    en="Program Type",
                ),
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                        ),
                    )
                    for slug, title_fi, title_en in [
                        ("performance", "Esitys", "Performance"),
                        ("experience", "Kokemus", "Experience"),
                        ("meetup", "Miitti", "Meetup"),
                        ("gaming", "Pelaaminen", "Gaming"),
                        ("talk", "Puheohjelma", "Talk"),
                        ("activity", "Liikunnallinen", "Activity"),
                        ("workshop", "Työpaja", "Workshop"),
                        ("exhibit", "Näyttely", "Exhibit"),
                    ]
                ],
            ),
            DimensionDTO(
                slug="room",
                title=ROOM_DIMENSION_TITLE_LOCALIZED,
                choices=[
                    DimensionValueDTO(slug=room.slug, title={self.language: room.name})
                    for room in Room.objects.filter(event=self.event)
                ],
            ),
        ]

    def get_program_dimension_values(self, programme: Programme) -> dict[str, str | list[str] | None]:
        return dict(
            date=self.get_date_dimension_value(programme),
            type=self.get_type_dimension_value(programme),
            room=programme.room.slug if programme.room else None,
        )

    def get_type_dimension_value(self, programme: Programme) -> list[str]:
        values = set()
        cat_title_fi = programme.category.title.split("/", 1)[0].strip()
        prog_title_lower = programme.title.lower()

        if cat_title_fi == "Esitysohjelma":
            values.add("performance")

        if cat_title_fi in (
            "Kokemuspiste: avoin pelautus",
            "Kokemuspiste: demotus",
            "Kokemuspiste: muu",
        ):
            values.add("experience")

        if cat_title_fi == "Miitti":
            values.add("meetup")

        if cat_title_fi in (
            "Figupelit: avoin pelautus",
            "Figupelit: demotus",
            "Kokemuspiste: avoin pelautus",
            "Kokemuspiste: demotus",
            "LARP",
            "Muu peliohjelma",
            "Roolipeli",
            "Turnaukset: figupelit",
            "Turnaukset: korttipelit",
            "Turnaukset: lautapelit",
            "Turnaukset: muu",
        ):
            values.add("gaming")

        if cat_title_fi in (
            "Puheohjelma: esitelmä",
            "Puheohjelma: paneeli",
            "Puheohjelma: keskustelu",
        ):
            values.add("talk")

        if cat_title_fi == "Tanssiohjelma" or "boff" in prog_title_lower or "polttopallo" in prog_title_lower:
            values.add("activity")

        if cat_title_fi in (
            "Työpaja: figut",
            "Työpaja: käsityö",
            "Työpaja: musiikki",
            "Työpaja: muu",
        ):
            values.add("workshop")

        if "näyttely" in prog_title_lower:
            values.add("exhibit")

        return list(values)

    def get_other_fields(self, programme: Programme) -> dict[str, str]:
        other_fields = super().get_other_fields(programme)

        other_fields.update(
            **{
                "ropecon:rpgSystem": programme.rpg_system,
                "ropecon:otherAuthor": programme.other_author,
                "konsti:minAttendance": programme.min_players,
                "konsti:maxAttendance": programme.max_players,
                "ropecon:numCharacters": programme.ropecon2018_characters,
                "ropecon:workshopFee": programme.ropecon2023_workshop_fee,
                "ropecon:contentWarnings": programme.ropecon2022_content_warnings,
                "ropecon:accessibilityOther": programme.ropecon2023_other_accessibility_information,
            }
        )

        return other_fields
