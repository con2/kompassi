from __future__ import annotations

import logging
from datetime import timedelta

from django.db import models
from django.utils.timezone import get_current_timezone

from core.models import Event
from core.utils.model_utils import slugify
from programme.models.category import Category
from programme.models.programme import PROGRAMME_STATES_LIVE, Programme
from programme.models.room import Room
from programme.models.tag import Tag

from ..models.dimension import DimensionDTO, DimensionValueDTO, ProgramDimensionValue
from ..models.program import Program
from ..models.schedule import ScheduleItem

logger = logging.getLogger("kompassi")
tz = get_current_timezone()


def normalislug(slug: str) -> str:
    slug = slugify(slug)
    slug = slug.removeprefix("a-week-")
    return slug.removesuffix("-")


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


def get_room_value(programme: Programme):
    return normalislug(programme.room.slug) if programme.room else None


def get_signup_value(programme: Programme):
    if programme.signup_link:
        return "konsti" if "konsti" in programme.signup_link else "other"
    return "no"


def get_start_time(programme: Programme):
    if programme.start_time:
        if programme.title == "Breakfast 06:30 - 10:00":
            return programme.start_time.replace(hour=6, minute=30, tzinfo=tz)
        elif programme.title == "Breakfast 07:00 - 10:00":
            return programme.start_time.replace(hour=7, minute=00, tzinfo=tz)

    return programme.start_time


def get_length(programme: Programme):
    if programme.title == "Breakfast 06:30 - 10:00":
        return timedelta(hours=3, minutes=30)
    elif programme.title == "Breakfast 07:00 - 10:00":
        return timedelta(hours=3)

    return timedelta(minutes=programme.length) if programme.length else None


def ensure_solmukohta2024_dimensions(event: Event):
    """
    NOTE: It is your responsibility to call Program.refresh_cached_dimensions() after calling this method.
    """
    dimensions = [
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
                DimensionValueDTO(slug=normalize_sk_type_value(category.slug), title={"en": category.title})
                for category in Category.objects.filter(event=event).exclude(slug="aweek-program")
            ],
        ),
        DimensionDTO(
            slug="aw-type",
            title={"en": "Program type (A Week)", "fi": "Ohjelman tyyppi (A Week)"},
            choices=[
                DimensionValueDTO(slug=normalislug(tag.slug), title={"en": tag.title[len("A Week - ") :]})
                for tag in Tag.objects.filter(event=event, title__startswith="A Week")
            ],
        ),
        DimensionDTO(
            slug="room",
            title={"en": "Room", "fi": "Sali"},
            choices=[
                DimensionValueDTO(slug=room.slug, title={"en": room.name}) for room in Room.objects.filter(event=event)
            ],
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

    DimensionDTO.save_many(event, dimensions)


def import_solmukohta2024(event: Event, queryset: models.QuerySet[Programme]):
    ensure_solmukohta2024_dimensions(event)

    v1_programmes = [programme for programme in queryset.order_by("id") if programme.state in PROGRAMME_STATES_LIVE]

    program_upsert = [
        Program(
            event=programme.category.event,
            slug=programme.slug,
            title=programme.title,
            description=programme.description,
            other_fields=dict(
                formatted_hosts=programme.formatted_hosts,
                signup_link=programme.signup_link,
            ),
        )
        for programme in v1_programmes
    ]
    v2_programs = Program.objects.bulk_create(
        program_upsert,
        update_conflicts=True,
        unique_fields=("event", "slug"),
        update_fields=("title", "description", "other_fields"),
    )

    # cannot use ScheduleItem.objects.bulk_create(…, update_conflicts=True)
    # because there is no unique constraint
    ScheduleItem.objects.filter(program__in=v2_programs).delete()
    schedule_upsert = [
        ScheduleItem(
            program=v2_program,
            start_time=get_start_time(v1_programme),
            length=get_length(v1_programme),
        )
        for v1_programme, v2_program in zip(v1_programmes, v2_programs, strict=True)
        if v1_programme.start_time is not None and v1_programme.length is not None
    ]
    ScheduleItem.objects.bulk_create(schedule_upsert)

    upsert_cache = ProgramDimensionValue.build_upsert_cache(event)
    pdv_upsert = [
        item
        for programme, program_v2 in zip(v1_programmes, v2_programs, strict=True)
        for item in ProgramDimensionValue.build_upsertables(
            program_v2,
            {
                "date": programme.start_time.date().isoformat() if programme.start_time else None,
                "event": get_event_value(programme),
                "sk-type": get_sk_type_value(programme),
                "aw-type": get_aw_type_value(programme),
                "room": get_room_value(programme),
                "signup": get_signup_value(programme),
            },
            *upsert_cache,
        )
    ]
    ProgramDimensionValue.bulk_upsert(pdv_upsert)
    Program.refresh_cached_dimensions_qs(event.programs.all())

    return v2_programs
