from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import time, timedelta

from django.utils.timezone import get_current_timezone

from core.models import Event
from core.utils.model_utils import slugify
from programme.models.category import Category
from programme.models.programme import Programme
from programme.models.tag import Tag

from ..consts import DEFAULT_COLORS
from ..models.dimension import DimensionDTO, DimensionValueDTO
from .default import DefaultImporter

logger = logging.getLogger("kompassi")
tz = get_current_timezone()


def normalislug(slug: str) -> str:
    slug = slugify(slug)
    slug = slug.removeprefix("a-week-")
    return slug.removesuffix("-")


def get_date_value(programme: Programme):
    if programme.start_time is None:
        return None

    date = programme.start_time.date()

    # programs starting as late as 2AM are considered to be part of the previous day
    if programme.start_time.time() < time(2, 0):
        date -= timedelta(days=1)

    return date.isoformat()


def get_event_value(programme: Programme):
    return "aweek" if programme.category.slug == "aweek-program" else "solmukohta"


def normalize_sk_type_value(category_slug: str) -> str:
    slug = normalislug(category_slug)
    return "talk" if slug == "talk-lecture-lightning-talks-etc" else slug


def get_sk_type_value(programme: Programme):
    if (category_slug := programme.category.slug) == "aweek-program":
        return None
    return normalize_sk_type_value(category_slug)


def get_aw_type_value(programme: Programme):
    if programme.category.slug != "aweek-program":
        return None

    tag = programme.tags.filter(title__startswith="A Week ").first()
    if tag is None:
        return None

    return normalislug(tag.slug)


def get_room_choices(event: Event):
    rooms = {
        programme.room.slug: programme.room
        for programme in Programme.objects.filter(category__event=event).exclude(category__slug="aweek-program")
        if programme.room
    }

    return [DimensionValueDTO(slug=normalislug(room.slug), title={"en": room.name}) for room in rooms.values()]


def get_room_value(programme: Programme):
    if programme.category.slug == "aweek-program":
        return None

    return normalislug(programme.room.slug) if programme.room else None


def get_signup_value(programme: Programme):
    if programme.signup_link:
        return "konsti" if "konsti" in programme.signup_link else "other"
    return "no"


@dataclass
class SolmukohtaImporter(DefaultImporter):
    event: Event
    language: str = "en"

    def get_start_time(self, programme: Programme):
        start_time = super().get_start_time(programme)

        if programme.title == "Breakfast 06:30 - 10:00":
            return start_time.replace(hour=6, minute=30, tzinfo=tz)
        elif programme.title == "Breakfast 07:00 - 10:00":
            return start_time.replace(hour=7, minute=00, tzinfo=tz)

        return start_time

    def get_length(self, programme: Programme):
        if programme.title == "Breakfast 06:30 - 10:00":
            return timedelta(hours=3, minutes=30)
        elif programme.title == "Breakfast 07:00 - 10:00":
            return timedelta(hours=3)

        return super().get_length(programme)

    def get_dimensions(self):
        return [
            DimensionDTO(
                slug="date",
                title={"en": "Day", "fi": "Päivä"},
                choices=[
                    DimensionValueDTO(slug="2024-04-08", title={"en": "Monday", "fi": "maanantai"}),
                    DimensionValueDTO(slug="2024-04-09", title={"en": "Tuesday", "fi": "tiistai"}),
                    DimensionValueDTO(slug="2024-04-10", title={"en": "Wednesday", "fi": "keskiviikko"}),
                    DimensionValueDTO(slug="2024-04-11", title={"en": "Thursday", "fi": "torstai"}),
                    DimensionValueDTO(slug="2024-04-12", title={"en": "Friday", "fi": "perjantai"}),
                    DimensionValueDTO(slug="2024-04-13", title={"en": "Saturday", "fi": "lauantai"}),
                    DimensionValueDTO(slug="2024-04-14", title={"en": "Sunday", "fi": "sunnuntai"}),
                ],
            ),
            DimensionDTO(
                slug="event",
                title={"en": "Event", "fi": "Tapahtuma"},
                choices=[
                    DimensionValueDTO(
                        slug="solmukohta",
                        title={"en": "Solmukohta", "fi": "Solmukohta"},
                    ),
                    DimensionValueDTO(
                        slug="aweek",
                        title={"en": "A Week in Finland", "fi": "A Week in Finland"},
                    ),
                ],
            ),
            DimensionDTO(
                slug="sk-type",
                title={"en": "Program type (Solmukohta)", "fi": "Ohjelman tyyppi (Solmukohta)"},
                choices=[
                    DimensionValueDTO(
                        slug=normalize_sk_type_value(category.slug),
                        title={"en": category.title},
                        color=DEFAULT_COLORS.get(category.style, ""),
                    )
                    for category in Category.objects.filter(event=self.event).exclude(slug="aweek-program")
                ],
            ),
            DimensionDTO(
                slug="aw-type",
                title={"en": "Program type (A Week)", "fi": "Ohjelman tyyppi (A Week)"},
                choices=[
                    DimensionValueDTO(
                        slug=normalislug(tag.slug),
                        title={"en": tag.title[len("A Week - ") :]},
                        color=DEFAULT_COLORS["color6"],
                    )
                    for tag in Tag.objects.filter(event=self.event, title__startswith="A Week")
                ],
            ),
            DimensionDTO(
                slug="room",
                title={"en": "Room (Solmukohta)", "fi": "Sali (Solmukohta)"},
                choices=get_room_choices(self.event),
            ),
            DimensionDTO(
                slug="signup",
                title={"en": "Advance signup", "fi": "Ennakkoilmoittautuminen"},
                choices=[
                    DimensionValueDTO(slug="konsti", title={"en": "Yes, in Konsti", "fi": "Kyllä, Konstin kautta"}),
                    DimensionValueDTO(slug="other", title={"en": "Yes, elsewhere", "fi": "Kyllä, muuta kautta"}),
                    DimensionValueDTO(slug="no", title={"en": "None", "fi": "Ei"}),
                ],
            ),
        ]

    def get_program_dimension_values(self, programme: Programme) -> dict[str, str | list[str] | None]:
        return {
            "date": get_date_value(programme),
            "event": get_event_value(programme),
            "sk-type": get_sk_type_value(programme),
            "aw-type": get_aw_type_value(programme),
            "room": get_room_value(programme),
            "signup": get_signup_value(programme),
        }
