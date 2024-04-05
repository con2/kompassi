from __future__ import annotations

import logging
from datetime import timedelta

from django.conf import settings
from django.db import models

from core.models import Event
from core.utils.model_utils import EnsuranceCompany, slugify
from programme.models.category import Category
from programme.models.programme import PROGRAMME_STATES_LIVE, Programme
from programme.models.room import Room
from programme.models.tag import Tag

from ..models.dimension import Dimension, DimensionDTO, DimensionValueDTO, ProgramDimensionValue
from ..models.program import Program
from ..models.schedule import ScheduleItem

logger = logging.getLogger("kompassi")


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


def ensure_solmukohta2024_dimensions(event: Event):
    """
    NOTE: It is your responsibility to call Program.refresh_cached_dimensions() after calling this method.
    """
    dimensions = [
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
            title={"en": "Program type (SK)", "fi": "Ohjelman tyyppi (SK)"},
            choices=[
                DimensionValueDTO(slug=normalize_sk_type_value(category.slug), title={"en": category.title})
                for category in Category.objects.filter(event=event).exclude(slug="aweek-program")
            ],
        ),
        DimensionDTO(
            slug="aw-type",
            title={"en": "Program type (AW)", "fi": "Ohjelman tyyppi (AW)"},
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
    ]

    DimensionDTO.save_many(event, dimensions)

    if settings.DEBUG:
        Dimension.dump_dimensions(event)


def import_solmukohta2024(event: Event, queryset: models.QuerySet[Programme]):
    ensure_solmukohta2024_dimensions(event)

    v1_programmes = [programme for programme in queryset.order_by("id") if programme.state in PROGRAMME_STATES_LIVE]

    ensure_unique_slug = EnsuranceCompany()
    program_upsert = [
        Program(
            event=programme.category.event,
            slug=ensure_unique_slug(programme.slug),
            title=programme.title,
            description=programme.description,
            other_fields=dict(formatted_hosts=programme.formatted_hosts),
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
            start_time=v1_programme.start_time,
            length=timedelta(seconds=v1_programme.length * 60),
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
                "event": get_event_value(programme),
                "sk-type": get_sk_type_value(programme),
                "aw-type": get_aw_type_value(programme),
                "room": get_room_value(programme),
            },
            *upsert_cache,
        )
    ]
    ProgramDimensionValue.bulk_upsert(pdv_upsert)
    Program.refresh_cached_dimensions_qs(event.programs.all())

    return v2_programs
