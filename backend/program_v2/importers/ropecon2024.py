from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from django.utils.timezone import get_current_timezone

from core.models import Event
from programme.models.programme import Programme

from ..consts import DATE_DIMENSION_TITLE_LOCALIZED, ROOM_DIMENSION_TITLE_LOCALIZED
from ..integrations.konsti import KONSTI_DIMENSION_DTO
from ..models.dimension import DimensionDTO, DimensionValueDTO, ValueOrdering
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
                value_ordering=ValueOrdering.SLUG,
                choices=list(self._get_date_dimension_values()),
            ),
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
                        ),
                    )
                    for slug, title_fi, title_en in [
                        ("performance", "Esitys", "Performance"),
                        ("experience", "Kokemus", "Experience"),
                        ("meetup", "Miitti", "Meetup"),
                        ("gaming", "Pelaaminen", "Gaming"),
                        ("open-gaming", "Avoin pelaaminen", "Open gaming"),
                        ("demo", "Demo", "Demo"),
                        ("tournament", "Turnaus", "Tournament"),
                        ("talk", "Puheohjelma", "Talk"),
                        ("presentation", "Esitelmä", "Presentation"),
                        ("discussion", "Keskustelu", "Discussion group"),
                        ("panel", "Paneeli", "Panel discussion"),
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
                        ("theme", "Hirviöt", "Monsters"),
                    ]
                ],
            ),
            DimensionDTO(
                slug="room",
                title=ROOM_DIMENSION_TITLE_LOCALIZED,
                choices=list(self._get_room_dimension_values()),
            ),
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
                        (
                            "loud-sounds",
                            "Kovat äänet",
                            "Loud sounds",
                        ),
                        (
                            "flashing-lights",
                            "Välkkyvät tai voimakkaat valot",
                            "Flashing or bright lights",
                        ),
                        (
                            "strong-smells",
                            "Voimakkaat tuoksut",
                            "Strong smells",
                        ),
                        (
                            "irritate-skin",
                            "Ihoa ärsyttävät aineet tai materiaalit",
                            "Materials or substances that irritate the skin",
                        ),
                        (
                            "physical-contact",
                            "Fyysinen kontakti ja/tai suppea henkilökohtaisen tilan mahdollisuus",
                            "Physical contact and/or low chances or personal space",
                        ),
                        (
                            "low-lighting",
                            "Pimeä/heikko valaistus",
                            "Darkness/low lighting",
                        ),
                        (
                            "moving-around",
                            "Paljon liikkumista ilman mahdollisuutta istumiseen",
                            "A lot of moving around without a chance for sitting down",
                        ),
                        (
                            "duration-over-2h",
                            "Kesto yli 2 tuntia ilman taukoja",
                            "Duration over two hours withtout breaks",
                        ),
                        (
                            "limited-moving-opportunities",
                            "Rajatut mahdollisuudet liikkumiseen",
                            "Limited opportunies to move around",
                        ),
                        (
                            "video",
                            "Video, jossa ei ole tekstitystä kuulorajoitteisille",
                            "Video without subtitles for the hearing impaired",
                        ),
                        (
                            "recording",
                            "Äänite, josta ei ole tekstiversiota kuulorajoitteisille",
                            "Recording without a text version for the hearing impaired",
                        ),
                        (
                            "long-texts",
                            "Pitkien tekstien itsenäistä lukemista",
                            "Reading long texts independently",
                        ),
                        (
                            "texts-with-no-recordings",
                            "Tekstiä, josta ei ole saatavilla nauhoitetta tai jota ei lueta ääneen",
                            "Text essential to participation without a recoding or text read out loud",
                        ),
                        (
                            "requires-dexterity",
                            "Vaatii sorminäppäryyttä",
                            "Requires dexterity",
                        ),
                        (
                            "requires-quick-reactions",
                            "Vaatii nopeaa reaktiokykyä",
                            "Requires ability to react quickly",
                        ),
                        (
                            "colorblind",
                            "Materiaalit voivat tuottaa haasteita värisokeille",
                            "Materials used can cause problems for the colourblind",
                        ),
                    ]
                ],
            ),
            DimensionDTO(
                slug="audience",
                title=dict(fi="Kohderyhmä", en="Target Audience", sv="Målgrupp"),
                value_ordering=ValueOrdering.MANUAL,
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                        ),
                    )
                    for slug, title_fi, title_en in [
                        ("all-ages", "Sopii kaiken ikäisille", "Suitable for all ages"),
                        ("aimed-under-13", "Suunnattu alle 13-vuotiaille", "Aimed at children under 13"),
                        ("aimed-between-13-17", "Suunnattu 13–17-vuotiaille", "Aimed at children between 13–17"),
                        ("aimed-adults", "Suunnattu täysi-ikäisille", "Aimed at adult attendees"),
                        ("k-18", "Vain täysi-ikäisille", "For 18+ only"),
                        ("beginners", "Aloittelijaystävällinen", "Beginner-friendly"),
                    ]
                ],
            ),
            DimensionDTO(
                slug="playstyle",
                title=dict(fi="Pelityyli", en="Playstyle", sv="Spelstil"),
                value_ordering=ValueOrdering.MANUAL,
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                        ),
                    )
                    for slug, title_fi, title_en in [
                        ("serious", "Vakava", "Serious"),
                        ("light", "Kevyt", "Light"),
                        ("rules-heavy", "Raskaat säännöt", "Rules-heavy"),
                        ("rules-light", "Kevyet säännöt", "Rules-light"),
                        ("story-driven", "Tarinavetoinen", "Story-driven"),
                        ("character-driven", "Hahmovetoinen", "Character-driven"),
                        ("combat-driven", "Taisteluvetoinen", "Combat-heavy"),
                    ]
                ],
            ),
            DimensionDTO(
                slug="language",
                title=dict(fi="Kieli", en="Language", sv="Språk"),
                value_ordering=ValueOrdering.MANUAL,
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                        ),
                    )
                    for slug, title_fi, title_en in [
                        ("fi", "Suomi", "Finnish"),
                        ("en", "Englanti", "English"),
                        ("sv", "Ruotsi", "Swedish"),
                        ("free", "Kielivapaa", "Language free"),
                    ]
                ],
            ),
            KONSTI_DIMENSION_DTO,
        ]

    def get_program_dimension_values(self, programme: Programme) -> dict[str, list[str]]:
        values = super().get_program_dimension_values(programme)
        prog_title_lower = programme.title.lower()
        other_lang_lower = programme.ropecon2024_language_other.lower()

        konsti_values = values.get("konsti", [])
        if (
            any((val in konsti_values) for val in ["tournament", "experiencePoint", "other"])
            and programme.ropecon2023_signuplist != "konsti"
        ):
            values["konsti"] = []

        if "näyttely" in prog_title_lower:
            values.setdefault("type", []).append("exhibit")

        if programme.ropecon_theme:
            values.setdefault("topic", []).append("theme")

        # accessibility
        if programme.ropecon2021_accessibility_loud_sounds:
            values.setdefault("accessibility", []).append("loud-sounds")

        if programme.ropecon2021_accessibility_flashing_lights:
            values.setdefault("accessibility", []).append("flashing-lights")

        if programme.ropecon2021_accessibility_strong_smells:
            values.setdefault("accessibility", []).append("strong-smells")

        if programme.ropecon2021_accessibility_irritate_skin:
            values.setdefault("accessibility", []).append("irritate-skin")

        if programme.ropecon2021_accessibility_physical_contact:
            values.setdefault("accessibility", []).append("physical-contact")

        if programme.ropecon2021_accessibility_low_lightning:
            values.setdefault("accessibility", []).append("low-lighting")

        if programme.ropecon2021_accessibility_moving_around:
            values.setdefault("accessibility", []).append("moving-around")

        if programme.ropecon2023_accessibility_programme_duration_over_2_hours:
            values.setdefault("accessibility", []).append("duration-over-2h")

        if programme.ropecon2023_accessibility_limited_opportunities_to_move_around:
            values.setdefault("accessibility", []).append("limited-moving-opportunities")

        if programme.ropecon2021_accessibility_video:
            values.setdefault("accessibility", []).append("video")

        if programme.ropecon2021_accessibility_recording:
            values.setdefault("accessibility", []).append("recording")

        if programme.ropecon2023_accessibility_long_texts:
            values.setdefault("accessibility", []).append("long-texts")

        if programme.ropecon2023_accessibility_texts_not_available_as_recordings:
            values.setdefault("accessibility", []).append("texts-with-no-recordings")

        if programme.ropecon2023_accessibility_participation_requires_dexterity:
            values.setdefault("accessibility", []).append("requires-dexterity")

        if programme.ropecon2023_accessibility_participation_requires_react_quickly:
            values.setdefault("accessibility", []).append("requires-quick-reactions")

        if programme.ropecon2021_accessibility_colourblind:
            values.setdefault("accessibility", []).append("colorblind")

        # audience
        if programme.ropecon2023_suitable_for_all_ages:
            values.setdefault("audience", []).append("all-ages")
        if programme.ropecon2023_aimed_at_children_under_13:
            values.setdefault("audience", []).append("aimed-under-13")
        if programme.ropecon2023_aimed_at_children_between_13_17:
            values.setdefault("audience", []).append("aimed-between-13-17")
        if programme.ropecon2023_aimed_at_adult_attendees:
            values.setdefault("audience", []).append("aimed-adults")
        if programme.ropecon2023_for_18_plus_only:
            values.setdefault("audience", []).append("k-18")
        if programme.ropecon2023_beginner_friendly:
            values.setdefault("audience", []).append("beginners")

        # language
        if programme.ropecon2024_language == "finnish":
            values.setdefault("language", []).append("fi")

        if programme.ropecon2024_language == "english":
            values.setdefault("language", []).append("en")

        if programme.ropecon2024_language == "language_free":
            values.setdefault("language", []).append("free")

        if programme.ropecon2024_language == "fin_and_eng":
            values.setdefault("language", []).append("fi")
            values.setdefault("language", []).append("en")

        for language_name in ("ruots", "swedish", "svensk"):
            if language_name in other_lang_lower:
                values.setdefault("language", []).append("sv")

        if "suomi" in other_lang_lower:
            values.setdefault("language", []).append("fi")
        if "english" in other_lang_lower:
            values.setdefault("language", []).append("en")

        for v1_attribute, playstyle_slug in [
            ("ropecon2018_style_serious", "serious"),
            ("ropecon2018_style_light", "light"),
            ("ropecon2018_style_rules_heavy", "rules-heavy"),
            ("ropecon2018_style_rules_light", "rules-light"),
            ("ropecon2018_style_story_driven", "story-driven"),
            ("ropecon2018_style_character_driven", "character-driven"),
            ("ropecon2018_style_combat_driven", "combat-driven"),
        ]:
            if getattr(programme, v1_attribute):
                values.setdefault("playstyle", []).append(playstyle_slug)

        return values

    def get_program_annotations(self, programme: Programme) -> dict[str, Any]:
        annotations = super().get_program_annotations(programme)
        dimension_values = self.get_program_dimension_values(programme)

        is_konsti = len(dimension_values.get("konsti", [])) > 0
        if is_konsti:
            annotations["internal:links:signup"] = f"https://ropekonsti.fi/program/item/{programme.slug}"

        return annotations
