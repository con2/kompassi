import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
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
from ..models.program import Program
from ..models.schedule import ScheduleItem
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
                value_ordering=ValueOrdering.SLUG,
                choices=list(self._get_date_dimension_values()),
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
                choices=[
                    DimensionValueDTO(slug="fi", title=dict(fi="Suomi", en="Finnish", sv="Finska")),
                    DimensionValueDTO(slug="en", title=dict(fi="Englanti", en="English", sv="Engelska")),
                    # DimensionValueDTO(slug="free", title=dict(fi="Kielivapaa", en="Language free", sv="Språkfri")),
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
                        (
                            "rpg-desk",
                            "Ilmoittautuminen roolipelitiskillä",
                            "Registration at RPG desk",
                            "Anmälan vid rollspelsdisken",
                        ),
                        ("form", "Ilmoittautuminen lomakkeella", "Registration via form", "Anmälan via formulär"),
                    ]
                ],
            ),
            DimensionDTO(
                slug="tickets",
                title=dict(
                    fi="Pääsyliput",
                    en="Tickets",
                    sv="Biljetter",
                ),
                value_ordering=ValueOrdering.TITLE,
                choices=[
                    DimensionValueDTO(
                        slug=slug,
                        title=dict(
                            fi=title_fi,
                            en=title_en,
                            sv=title_sv,
                        ),
                    )
                    for slug, title_fi, title_en, title_sv in [
                        ("free", "Vapaa pääsy", "Free admission", "Fri entré"),
                        ("tracon", "Traconin pääsylipulla", "With Tracon ticket", "Med Tracons biljett"),
                        (
                            "party",
                            "Iltabileiden pääsylipulla",
                            "With evening party ticket",
                            "Med kvällsfestens biljett",
                        ),
                        ("special", "Erillisellä pääsylipulla", "With separate ticket", "Med separat biljett"),
                    ]
                ],
            ),
            KONSTI_DIMENSION_DTO,
        ]

    def get_program_dimension_values(self, programme: Programme) -> dict[str, list[str]]:
        base_annotations = super().get_program_annotations(programme)
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

        konsti = dimensions.setdefault("konsti", [])
        if (form := programme.form_used) and form.slug == "rpg":
            konsti.append("tabletopRPG")

        signup = set(dimensions.get("signup", []))
        if konsti:
            signup.add("konsti")
        if link := programme.signup_link:
            if "konsti" in link:
                signup.add("konsti")
            elif "lippu.fi" in link:
                signup.add("tickets")
            else:
                signup.add("form")
        if programme.is_using_paikkala:
            signup.add("paikkala")
        if base_annotations.get("konsti:isPlaceholder", False):
            signup.remove("konsti")
            if "roolipelitiskillä" in programme.description.lower():
                signup.add("rpg-desk")
        if not signup:
            signup.add("none")
        dimensions["signup"] = list(signup)

        tickets = set(dimensions.setdefault("tickets", []))
        if link := programme.signup_link and "lippu.fi" in link:
            tickets.add("special")
        if room := programme.room:
            if room.slug == "iltabileet":
                tickets.add("party")
            elif room.slug in ("boffausalue", "terastaistelualue", "tracon-live") or "Puisto " in room.name:
                tickets.add("free")
        if not tickets:
            tickets.add("tracon")
        dimensions["tickets"] = list(tickets)

        language = dimensions.setdefault("language", [])
        if not language:
            language.append("fi")

        return dimensions

    def get_program_annotations(self, programme: Programme) -> dict[str, Any]:
        annotations = super().get_program_annotations(programme)
        dimension_values = self.get_program_dimension_values(programme)

        konsti = dimension_values.get("konsti", [])
        if konsti and not annotations.get("konsti:isPlaceholder", False):
            if "fleamarket" in konsti:
                annotations["internal:links:signup"] = "https://ropekonsti.fi/program/list?programType=fleamarket"
                annotations["konsti:maxAttendance"] = 130
            else:
                annotations["internal:links:signup"] = f"https://ropekonsti.fi/program/item/{programme.slug}"

        if "lippu.fi" in programme.signup_link:
            annotations["internal:links:tickets"] = programme.signup_link
            annotations["internal:links:signup"] = ""

        if "paikkala" in dimension_values.get("signup", []):
            annotations["internal:links:reservation"] = "https://kompassi.eu/profile/reservations"

        if programme.slug == "arsenic-lies":
            annotations["konsti:minAttendance"] = 5
            annotations["konsti:maxAttendance"] = 10
        elif programme.slug == "muistojen-tanssi-larppi":
            annotations["konsti:minAttendance"] = 6
            annotations["konsti:maxAttendance"] = 9

        return annotations

    def get_fleamarket_schedule_item(
        self,
        v2_program: Program,
        start_time: datetime,
        end_time: datetime,
        slot_delta: timedelta,
        slot_length: timedelta,
    ) -> ScheduleItem:
        """
        We use Konsti for flea market time slot reservations.
        This is managed as one program per day, with 30-minute time slots for reservations.
        For technical reasons, the start and end times need to cover the whole period under which reservations are made.
        This lets Konsti understand that the time slots are mutually exclusive ie. the user should be enrolled in only one slot.
        The last slot is left out in order to flush the queue.
        """
        slot_start_time = start_time + slot_delta
        slot_end_time = slot_start_time + slot_length

        slot_start_time = slot_start_time.astimezone(tz)
        slot_end_time = slot_end_time.astimezone(tz)

        return ScheduleItem(
            slug=f"{v2_program.slug}-{slot_start_time.strftime('%H%M')}",
            subtitle=f"Saapuminen kello {slot_start_time.strftime('%H:%M')}–{slot_end_time.strftime('%H:%M')}",
            program=v2_program,
            start_time=start_time,
            length=slot_end_time - start_time,  # see https://ropecon.slack.com/archives/CNQG7QJG2/p1725188582924579
        ).with_generated_fields()

    def get_schedule_items(self, v1_programme: Programme, v2_program: Program) -> list[ScheduleItem]:
        """
        Return a list of unsaved V2 ScheduleItems for the V1 Programme.
        """
        if "kirpputorin-ajanvaraus" not in v1_programme.slug:
            return super().get_schedule_items(v1_programme, v2_program)

        # flea market gets special treatment, see docstring of get_fleamarket_schedule_item
        start_time = self.get_start_time(v1_programme)
        end_time = self.get_end_time(v1_programme)
        slot_minutes = 30
        slot_length = timedelta(minutes=slot_minutes)

        # we leave the last 30 min slot out in order to flush the queue
        # as range() is end exclusive, no need to subtract anything
        total_minutes = v1_programme.length if v1_programme.length else -1

        return [
            self.get_fleamarket_schedule_item(
                v2_program,
                start_time,
                end_time,
                timedelta(minutes=delta_minutes),
                slot_length,
            )
            for delta_minutes in range(0, total_minutes, slot_minutes)
        ]
