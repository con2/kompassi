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
                slug="participation",
                title=dict(
                    fi="Osallistumistapa",
                    en="Way of Participation",
                    sv="Deltagandetyp",
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
                        ("open-gaming", "Avoin pelaaminen", "Open gaming"),
                        ("demo", "Demo", "Demo"),
                        ("tournament", "Turnaus", "Tournament"),
                        ("presentation", "Esitelmä", "Presentation"),
                        ("discussion", "Keskustelu", "Discussion group"),
                        ("panel", "Paneeli", "Panel discussion"),
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

    def get_program_dimension_values(self, programme: Programme) -> dict[str, list[str]]:
        values = super().get_program_dimension_values(programme)
        prog_title_lower = programme.title.lower()

        if "boff" in prog_title_lower:
            values.setdefault("topic", []).append("boffering")
            values.setdefault("type", []).append("activity")

        if "näyttely" in prog_title_lower:
            values.setdefault("type", []).append("exhibit")

        if "polttopallo" in prog_title_lower:
            values.setdefault("type", []).append("activity")

        return values

    def get_other_fields(self, programme: Programme) -> dict[str, str]:
        other_fields = super().get_other_fields(programme)
        dimension_values = self.get_program_dimension_values(programme)

        is_konsti = len(dimension_values.get("konsti", [])) > 0
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
