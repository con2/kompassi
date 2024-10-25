import logging
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import timedelta

from django.utils.timezone import get_current_timezone

from core.models import Event
from program_v2.models.dimension import DimensionDTO, DimensionValueDTO, ValueOrdering
from programme.models.programme import Programme

from ..consts import DEFAULT_COLORS
from ..integrations.konsti import KONSTI_DIMENSION_DTO
from .default import DefaultImporter

logger = logging.getLogger("kompassi")
tz = get_current_timezone()


@dataclass
class HitpointImporter(DefaultImporter):
    """
    May it be forever known that I resisted the urge to call this class "HitpoImporter".
    """

    event: Event
    language: str = "fi"

    date_cutoff_time = timedelta(hours=4)  # 04:00 local time

    def _get_room_dimension_values(self) -> Iterable[DimensionValueDTO]:
        return [
            *super()._get_room_dimension_values(),
            DimensionValueDTO(slug="ropeluokka-1", title=dict(fi="Ropeluokka 1")),
            DimensionValueDTO(slug="ropeluokka-2", title=dict(fi="Ropeluokka 2")),
            DimensionValueDTO(slug="ropeluokka-3", title=dict(fi="Ropeluokka 3")),
        ]

    def get_dimensions(self) -> list[DimensionDTO]:
        return [
            self._get_date_dimension(),
            DimensionDTO(
                slug="type",
                title=dict(
                    fi="Ohjelmatyyppi",
                    en="Program Type",
                    sv="Programtyp",
                ),
                value_ordering=ValueOrdering.MANUAL,
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                            color=color,
                        ),
                    )
                    for slug, title_fi, title_en, color in [
                        ("gaming", "Pelaaminen", "Gaming", ""),
                        ("talk", "Puheohjelma", "Talk", DEFAULT_COLORS["color3"]),
                        ("workshop", "Työpaja", "Workshop", DEFAULT_COLORS["color7"]),
                    ]
                ],
            ),
            DimensionDTO(
                slug="topic",
                title=dict(
                    fi="Aihe",
                    en="Topic",
                    sv="Tema",
                ),
                value_ordering=ValueOrdering.TITLE,
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                        ),
                        color=color,
                    )
                    for slug, title_fi, title_en, color in [
                        ("miniatures", "Figupelit", "Miniature games", DEFAULT_COLORS["color6"]),
                        ("boardgames", "Lautapelit", "Board games", DEFAULT_COLORS["color2"]),
                        ("cardgames", "Korttipelit", "Card games", DEFAULT_COLORS["color5"]),
                        ("larp", "Larppaaminen", "LARP", DEFAULT_COLORS["color1"]),
                        ("penandpaper", "Pöytäroolipelit", "Pen & Paper RPG", DEFAULT_COLORS["color4"]),
                    ]
                ],
            ),
            self._get_room_dimension(),
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
                        # ("tickets", "Erilliset pääsyliput", "Separate tickets", "Separata biljetter"),
                        # ("paikkala", "Maksuttomat paikkaliput", "Free seating tickets", "Gratis sittplatsbiljetter"),
                        ("konsti", "Ilmoittautuminen Konstilla", "Registration via Konsti", "Anmälan via Konsti"),
                        (
                            "rpg-desk",
                            "Ilmoittautuminen roolipelitiskillä",
                            "Registration at RPG desk",
                            "Anmälan vid rollspelsdisken",
                        ),
                        # ("form", "Ilmoittautuminen lomakkeella", "Registration via form", "Anmälan via formulär"),
                    ]
                ],
            ),
            KONSTI_DIMENSION_DTO,
        ]

    def get_program_dimension_values(self, programme: Programme) -> dict[str, list[str]]:
        dimensions = super().get_program_dimension_values(programme)

        # introduce some hierarchy to rooms
        room_dimension_values = set(dimensions.get("room", []))
        if programme.room:
            if "Lautapelialue" in programme.room.name:
                room_dimension_values.add("lautapelialue")
            if "Ropeluokka 1" in programme.room.name:
                room_dimension_values.add("ropeluokka-1")
            if "Ropeluokka 2" in programme.room.name:
                room_dimension_values.add("ropeluokka-2")
            if "Ropeluokka 3" in programme.room.name:
                room_dimension_values.add("ropeluokka-3")
        dimensions["room"] = list(room_dimension_values)

        topic_dimension_values = set(dimensions.get("topic", []))

        type_dimension_values = set(dimensions.get("type", []))
        if not type_dimension_values:
            if programme.form_used and programme.form_used.slug in ("freeform", "rpg"):
                type_dimension_values.add("gaming")

            for slug in ("larp", "boardgames", "cardgames", "penandpaper"):
                if slug in topic_dimension_values:
                    type_dimension_values.add("gaming")
                    break
        dimensions["type"] = list(type_dimension_values)

        konsti_dimension_value = ""
        if "gaming" in type_dimension_values:
            if "penandpaper" in topic_dimension_values:
                konsti_dimension_value = "tabletopRPG"
            if "larp" in topic_dimension_values:
                konsti_dimension_value = "larp"
        if konsti_dimension_value:
            dimensions["konsti"] = [konsti_dimension_value]
            dimensions["signup"] = ["konsti"]
        else:
            dimensions["konsti"] = []
            dimensions["signup"] = ["none"]

        return dimensions
