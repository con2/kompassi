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
                    sv="Programtyp",
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
                slug="topic",
                title=dict(
                    fi="Teema",
                    en="Topic",
                    sv="Tema",
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
                        ("miniatures", "Figuurit", "Miniatures"),
                        ("boardgames", "Lautapelit", "Board games"),
                        ("cardgames", "Korttipelit", "Card games"),
                        ("crafts", "Käsityöt", "Crafts"),
                        ("dance", "Tanssi", "Dance"),
                        ("larp", "Larppaaminen", "LARP"),
                        ("music", "Musiikki", "Music"),
                        ("penandpaper", "Pöytäroolipelit", "Pen & Paper RPG"),
                        ("boffering", "Boffaus", "Boffering"),
                        ("goh", "Kunniavieraat", "Guests of Honor"),
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
            DimensionDTO(
                slug="konsti",
                is_list_filter=False,
                is_shown_in_detail=False,
                title=dict(
                    fi="Konsti-ilmoittautumistyyppi",
                    en="Konsti signup type",
                    sv="Konsti-anmälningstyp",
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
                        # note: camelCase slugs defined by Konsti, pending discussion for consistency in later events
                        ("tabletopRPG", "Pöytäroolipeli", "Tabletop RPG"),
                        ("larp", "Larppi", "LARP"),
                        ("tournament", "Turnaus", "Tournament"),
                        ("workshop", "Työpaja", "Workshop"),
                        ("experiencePoint", "Kokemuspiste", "Experience Point"),
                        ("other", "Muu", "Other"),
                    ]
                ],
            ),
        ]

    def get_program_dimension_values(self, programme: Programme) -> dict[str, str | list[str] | None]:
        return dict(
            date=self.get_date_dimension_value(programme),
            type=self.get_type_dimension_value(programme),
            topic=self.get_topic_dimension_value(programme),
            room=programme.room.slug if programme.room else None,
            konsti=self.get_konsti_dimension_value(programme),
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

    def get_topic_dimension_value(self, programme: Programme) -> list[str]:
        values = set()
        cat_title_fi = programme.category.title.split("/", 1)[0].strip()
        tag_titles_fi = [tag.title.split("/", 1)[0].strip() for tag in programme.tags.all()]
        prog_title_lower = programme.title.lower()

        if cat_title_fi in (
            "Figupelit: avoin pelautus",
            "Figupelit: demotus",
            "Turnaukset: figupelit",
            "Työpaja: figut",
        ):
            values.add("miniatures")

        if "Aihe: figupelit" in tag_titles_fi:
            values.add("miniatures")

        if cat_title_fi == "Turnaukset: lautapelit":
            values.add("boardgames")

        if "Aihe: lautapelit" in tag_titles_fi:
            values.add("boardgames")

        if cat_title_fi == "Turnaukset: korttipelit":
            values.add("cardgames")

        if cat_title_fi == "Työpaja: käsityö":
            values.add("crafts")

        if cat_title_fi == "Tanssiohjelma":
            values.add("dance")

        if cat_title_fi == "LARP":
            values.add("larp")

        if "Aihe: Larpit" in tag_titles_fi:
            values.add("larp")

        if cat_title_fi == "Työpaja: musiikki":
            values.add("music")

        if "boff" in prog_title_lower:
            values.add("boffering")

        if "Kunniavieras" in tag_titles_fi:
            values.add("goh")

        return list(values)

    def get_konsti_dimension_value(self, programme: Programme) -> list[str]:
        values = set()
        cat_title_fi = programme.category.title.split("/", 1)[0].strip()

        if cat_title_fi == "LARP":
            values.add("larp")

        if cat_title_fi == "Roolipeli":
            values.add("tabletopRPG")

        if cat_title_fi.startswith("Turnaukset:"):
            values.add("tournament")

        if cat_title_fi.startswith("Työpaja:"):
            values.add("workshop")

        if cat_title_fi.startswith("Kokemuspiste:"):
            values.add("experiencePoint")

        # TODO add special case programs with the "other" Konsti settings profile
        # They are in these categories, but not all program of these categories is included?
        if cat_title_fi in (
            "Muu peliohjelma",
            "Muu ohjelma",
            "Figupelit: demotus",
        ):
            values.add("other")

        return list(values)

    def get_other_fields(self, programme: Programme) -> dict[str, str]:
        other_fields = super().get_other_fields(programme)

        is_konsti = len(self.get_konsti_dimension_value(programme)) > 0
        if is_konsti:
            other_fields["internal:links:signup"] = f"https://ropekonsti.fi/program/item/{programme.slug}"

        other_fields.update(
            **{
                "konsti:rpgSystem": programme.rpg_system,
                "ropecon:otherAuthor": programme.other_author,
                "konsti:minAttendance": programme.min_players,
                "konsti:maxAttendance": programme.max_players,
                "ropecon:numCharacters": programme.ropecon2018_characters,
                "konsti:workshopFee": programme.ropecon2023_workshop_fee,
                "ropecon:contentWarnings": programme.ropecon2022_content_warnings,
                "ropecon:accessibilityOther": programme.ropecon2023_other_accessibility_information,
            }
        )

        return other_fields
