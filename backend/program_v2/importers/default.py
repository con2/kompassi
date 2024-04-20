from __future__ import annotations

import logging
from datetime import timedelta
from typing import Literal

from django.db import models

from core.models import Event
from programme.models.category import Category
from programme.models.programme import PROGRAMME_STATES_LIVE, Programme
from programme.models.room import Room
from programme.models.tag import Tag

from ..models.dimension import DimensionDTO, DimensionValueDTO, ProgramDimensionValue
from ..models.program import Program
from ..models.schedule import ScheduleItem

logger = logging.getLogger("kompassi")


def ensure_default_dimensions(event: Event, language: Literal["en", "fi"] = "fi"):
    """
    NOTE: It is your responsibility to call Program.refresh_cached_dimensions() after calling this method.
    """
    dimensions = [
        DimensionDTO(
            slug="category",
            title={"en": "Category", "fi": "Tyyppi"},
            choices=[
                DimensionValueDTO(slug=category.slug, title={language: category.title})
                for category in Category.objects.filter(event=event)
            ],
        ),
        DimensionDTO(
            slug="tag",
            title={"en": "Tag", "fi": "Tagi"},
            choices=[
                DimensionValueDTO(slug=tag.slug, title={language: tag.title}) for tag in Tag.objects.filter(event=event)
            ],
        ),
        DimensionDTO(
            slug="room",
            title={"en": "Room", "fi": "Sali"},
            choices=[
                DimensionValueDTO(slug=room.slug, title={language: room.name})
                for room in Room.objects.filter(event=event)
            ],
        ),
    ]

    DimensionDTO.save_many(event, dimensions)


def import_default(event: Event, queryset: models.QuerySet[Programme]):
    ensure_default_dimensions(event)

    v1_programmes = [programme for programme in queryset.order_by("id") if programme.state in PROGRAMME_STATES_LIVE]

    program_upsert = [
        Program(
            event=programme.category.event,
            slug=programme.slug,
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
            dict(
                category=programme.category.slug,
                tag=[tag.slug for tag in programme.tags.all()],
                room=programme.room.slug if programme.room else None,
            ),
            *upsert_cache,
        )
    ]
    ProgramDimensionValue.bulk_upsert(pdv_upsert)
    Program.refresh_cached_dimensions_qs(event.programs.all())

    return v2_programs
