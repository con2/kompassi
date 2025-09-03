from __future__ import annotations

import logging
from pathlib import Path
from typing import Self
from uuid import uuid4

import pydantic
from django.conf import settings
from django.db import transaction
from django.template.defaultfilters import truncatechars
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from paikkala.forms import ReservationForm as PaikkalaReservationForm
from paikkala.models import Program as PaikkalaProgram
from paikkala.models import Room as PaikkalaRoom
from paikkala.models import Row
from paikkala.utils.importer import import_zones, read_csv

from kompassi.core.models.event import Event
from kompassi.core.utils import horizontal_form_helper
from kompassi.core.utils.log_utils import log_get_or_create
from kompassi.core.utils.model_utils import slugify
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO, ValueOrdering
from kompassi.dimensions.models.dimension_value import DimensionValue
from kompassi.dimensions.models.enums import AnnotationDataType
from kompassi.program_v2.models.paikkala_room_mapping import PaikkalaRoomMapping

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


def paikkalize_room(event: Event, room: DimensionValue) -> PaikkalaRoom:
    """
    Note: Always creates a new PaikkalaRoom.
    Only call when you are actually initializing a PaikkalaProgram.
    """
    paikkala_room_mapping = PaikkalaRoomMapping.objects.filter(room_dimension_value=room).first()
    if paikkala_room_mapping:
        paikkala_room = paikkala_room_mapping.paikkala_room
        log_get_or_create(logger, paikkala_room, False)
        return paikkala_room

    with get_schema_path(event.venue.slug, room.slug).open(encoding="UTF-8") as f:
        row_csv_list = list(read_csv(f))

    # hack: dun wanna mess up with same-named rooms
    room_name = str(uuid4())

    zones = import_zones(
        row_csv_list=row_csv_list,
        default_room_name=room_name,
    )
    paikkala_room = zones[0].room
    paikkala_room.name = room.get_title("fi")
    paikkala_room.save(update_fields=["name"])

    PaikkalaRoomMapping.objects.create(room_dimension_value=room, paikkala_room=paikkala_room)

    log_get_or_create(logger, paikkala_room, True)
    return paikkala_room


@transaction.atomic
def paikkalize_schedule_item(schedule_item: ScheduleItem) -> PaikkalaProgram:
    meta = schedule_item.program.meta
    tz = schedule_item.event.timezone

    (room_slug,) = schedule_item.cached_combined_dimensions.get("paikkala", [""])
    if not room_slug:
        raise ValueError("paikkalize_schedule_item a schedule item that is not using Paikkala?!? Preposterous!!!")

    # TODO configure reservation start time via annotations
    # reservation_start = schedule_item.cached_combined_annotations.get("paikkala:reservationStartDateTime")
    if settings.DEBUG:
        reservation_start = now()
    else:
        reservation_start = schedule_item.start_time.replace(hour=9, minute=0, tzinfo=tz)

    attrs = dict(
        event_name=schedule_item.event.name,
        name=truncatechars(schedule_item.title, PaikkalaProgram._meta.get_field("name").max_length),  # type: ignore
        require_user=True,
        reservation_start=reservation_start,
        reservation_end=schedule_item.cached_end_time,
        invalid_after=schedule_item.cached_end_time,
        max_tickets=0,
        automatic_max_tickets=True,
        max_tickets_per_user=meta.paikkala_default_max_tickets_per_user,
        max_tickets_per_batch=meta.paikkala_default_max_tickets_per_batch,
    )

    paikkala_program = PaikkalaProgram.objects.filter(kompassi_v2_schedule_item=schedule_item).first()
    if paikkala_program:
        log_get_or_create(logger, paikkala_program, False)

        for k, v in attrs.items():
            setattr(paikkala_program, k, v)
        paikkala_program.save(update_fields=attrs.keys())

        return paikkala_program

    room_sdv = schedule_item.dimensions.get(value__dimension__slug="room")
    paikkala_room = paikkalize_room(schedule_item.event, room_sdv.value)
    paikkala_program = PaikkalaProgram(room=paikkala_room, **attrs)
    paikkala_program.save()
    log_get_or_create(logger, paikkala_program, True)

    schedule_item.paikkala_program = paikkala_program
    schedule_item.paikkala_special_reservation_code = uuid4()
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


class ReservationForm(PaikkalaReservationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # make these translatable
        self.fields["zone"].label = _("Zone")
        self.fields["zone"].label_format = _("{zone} – {remaining} seats remain")  # type: ignore
        self.fields["count"].label = _("Count")
        self.fields["count"].help_text = _("You can reserve at most {max_tickets} tickets.").format(
            max_tickets=self.instance.max_tickets_per_batch,
        )

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False


# for ”special” tickets
class FakeRow(pydantic.BaseModel):
    name: str = "Rivi 1"


class FakeTicket(pydantic.BaseModel):
    row: FakeRow
    number: str = "Numeroimaton"

    @classmethod
    def come_into_being(cls) -> list[Self]:
        return [cls(row=FakeRow())]
