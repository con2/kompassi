from __future__ import annotations

import logging
from pathlib import Path

from django.template.defaultfilters import truncatechars
from paikkala.models import Program as PaikkalaProgram
from paikkala.models import Room as PaikkalaRoom
from paikkala.models import Row
from paikkala.utils.importer import import_zones, read_csv

from kompassi.core.models.event import Event
from kompassi.core.utils.model_utils import slugify
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO, ValueOrdering
from kompassi.dimensions.models.enums import AnnotationDataType

from ..models.schedule_item import ScheduleItem

logger = logging.getLogger(__name__)


def get_schema_path(venue_slug: str, room_slug: str) -> Path:
    _venue_slug = slugify(venue_slug)
    _room_slug = slugify(room_slug)

    if _venue_slug != venue_slug:
        raise ValueError("Invalid venue slug")

    if _room_slug != room_slug:
        raise ValueError("Invalid room slug")

    return Path(__file__).parent / "paikkala_data" / _venue_slug / f"{_room_slug}.csv"


def get_available_room_slugs(venue_slug: str):
    """
    >>> get_available_room_slugs("tampere-talo")
    ['iso-sali']
    """
    return [path.stem for path in get_schema_path(venue_slug, "dummy").parent.glob("*.csv") if path.stem]


def get_paikkala_dimension(event: Event) -> DimensionDTO | None:
    available_room_slugs = get_available_room_slugs(event.venue.slug)
    if not available_room_slugs:
        return None

    # TODO yeet another special kind of technical dimension:
    # it may be specified on a program by an admin user, BUT
    # its values may not be touched by them
    return DimensionDTO(
        slug="paikkala",
        is_list_filter=True,
        is_shown_in_detail=False,
        is_public=False,
        can_values_be_added=False,
        is_technical=True,  # TODO
        title=dict(
            fi="Paikkaliput (Paikkala)",
            en="Seat reservations (Paikkala)",
        ),
        value_ordering=ValueOrdering.MANUAL,
        choices=[
            DimensionValueDTO(
                slug=slug,
                is_technical=True,
                title=dict(
                    fi=slug,
                    en=slug,
                ),
            )
            for slug in available_room_slugs
        ],
    )


def get_paikkala_room(event: Event, room_slug: str) -> PaikkalaRoom:
    # hack: dun wanna mess up with same-named rooms
    venue_slug = event.venue.slug
    paikkala_room_name = f"{event.slug}/{room_slug}"

    existing_room = PaikkalaRoom.objects.filter(event__slug=event.slug, slug=room_slug).first()
    if existing_room:
        logger.info("Room %s is alredy paikkalized, not re-paikkalizing", existing_room)
        return existing_room

    with get_schema_path(venue_slug, room_slug).open(encoding="UTF-8") as f:
        row_csv_list = list(read_csv(f))

    import_zones(
        row_csv_list=row_csv_list,
        default_room_name=paikkala_room_name,
    )

    return PaikkalaRoom.objects.get(name=paikkala_room_name)


def paikkalize_schedule_item(schedule_item: ScheduleItem) -> PaikkalaProgram:
    meta = schedule_item.program.meta
    (room_slug,) = schedule_item.cached_combined_dimensions.get("paikkala", [""])
    paikkala_room = get_paikkala_room(schedule_item.event, room_slug)
    tz = schedule_item.event.timezone

    # TODO configure reservation start time via annotations
    # reservation_start = schedule_item.cached_combined_annotations.get("paikkala:reservationStartDateTime")

    paikkala_program, created = PaikkalaProgram.objects.update_or_create(
        kompassi_v2_schedule_item=schedule_item,
        defaults=dict(
            event_name=schedule_item.event.name,
            name=truncatechars(schedule_item.title, PaikkalaProgram._meta.get_field("name").max_length),  # type: ignore
            room=paikkala_room,
            require_user=True,
            reservation_start=schedule_item.start_time.replace(hour=9, minute=0, tzinfo=tz),
            reservation_end=schedule_item.cached_end_time,
            invalid_after=schedule_item.cached_end_time,
            max_tickets=0,
            automatic_max_tickets=True,
            max_tickets_per_user=meta.paikkala_default_max_tickets_per_user,
            max_tickets_per_batch=meta.paikkala_default_max_tickets_per_batch,
        ),
    )

    if created:
        schedule_item.paikkala_program = paikkala_program
        schedule_item.save(update_fields=["paikkala_program"])

        paikkala_program.rows.set(Row.objects.filter(zone__room=paikkala_room))
        paikkala_program.full_clean()
        paikkala_program.save()

    return paikkala_program


PAIKKALA_ANNOTATION_DTOS = [
    AnnotationDTO(
        slug="paikkala:reservationStartsAt",
        type=AnnotationDataType.DATETIME,
        title=dict(
            fi="Varauksen alkamisaika",
            en="Reservation start time",
            sv="Början av reservation",
        ),
    ),
]
