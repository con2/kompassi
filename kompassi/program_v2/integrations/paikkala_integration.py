from __future__ import annotations

import logging
from pathlib import Path
from typing import Self
from uuid import uuid4

import pydantic
from django.conf import settings
from django.db import transaction
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from paikkala.forms import ReservationForm as PaikkalaReservationForm
from paikkala.models.programs import Program as PaikkalaProgram
from paikkala.models.rooms import Room as PaikkalaRoom
from paikkala.models.rows import Row as PaikkalaRow
from paikkala.models.zones import Zone as PaikkalaZone
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

from ..filters import parse_datetime
from ..models.schedule_item import ScheduleItem

logger = logging.getLogger(__name__)


def get_schema_path(venue_slug: str, room_slug: str) -> Path:
    # guard against path traversal attacks
    _venue_slug = slugify(venue_slug)
    if _venue_slug != venue_slug:
        raise ValueError("Invalid venue slug")
    _room_slug = slugify(room_slug)
    if _room_slug != room_slug:
        raise ValueError("Invalid room slug")

    return Path(__file__).parent / "paikkala_data" / _venue_slug / f"{_room_slug}.csv"


def get_paikkala_room_slugs(venue_slug: str):
    """
    >>> get_available_room_slugs("tampere-talo")
    ['iso-sali']
    """
    return [path.stem for path in get_schema_path(venue_slug, "dummy").parent.glob("*.csv") if path.stem]


def get_paikkala_dimension(event: Event) -> DimensionDTO | None:
    available_room_slugs = get_paikkala_room_slugs(event.venue.slug)
    if not available_room_slugs:
        return None

    # HACK get names of the rooms from the room dimension
    # this might not work the first time as the room dimension is not yet loaded
    # so fallback to slug is needed
    if (
        (meta := event.program_v2_event_meta)
        and (cache := meta.universe.preload_dimensions())
        and (room_dvs_by_slug := cache.values_by_dimension.get("room"))
    ):
        room_names = {
            slug: room_dvs_by_slug[slug].title_dict if slug in room_dvs_by_slug else {"fi": slug}
            for slug in available_room_slugs
        }
    else:
        room_names = {slug: {"fi": slug} for slug in available_room_slugs}

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
                title=room_names[slug],
            )
            for slug in available_room_slugs
        ],
    )


def paikkalize_room(
    event: Event,
    paikkala_dimension_value: DimensionValue,
) -> PaikkalaRoom:
    """
    Note: Always creates a new PaikkalaRoom.
    Only call when you are actually initializing a PaikkalaProgram.
    """
    paikkala_room_mapping = PaikkalaRoomMapping.objects.filter(
        paikkala_dimension_value=paikkala_dimension_value
    ).first()
    if paikkala_room_mapping:
        paikkala_room = paikkala_room_mapping.paikkala_room
        log_get_or_create(logger, paikkala_room, False)
        return paikkala_room

    with get_schema_path(event.venue.slug, paikkala_dimension_value.slug).open(encoding="UTF-8") as f:
        row_csv_list = list(read_csv(f))

    # hack: dun wanna mess up with same-named rooms
    room_name = str(uuid4())

    zones = import_zones(
        row_csv_list=row_csv_list,
        default_room_name=room_name,
    )
    paikkala_room = zones[0].room
    paikkala_room.name = paikkala_dimension_value.get_title("fi")
    paikkala_room.save(update_fields=["name"])

    PaikkalaRoomMapping.objects.create(
        paikkala_dimension_value=paikkala_dimension_value,
        paikkala_room=paikkala_room,
    )

    log_get_or_create(logger, paikkala_room, True)
    return paikkala_room


@transaction.atomic
def paikkalize_schedule_item(
    schedule_item: ScheduleItem,
    **paikkalkwargs,
) -> PaikkalaProgram:
    meta = schedule_item.program.meta
    tz = schedule_item.event.timezone

    (room_slug,) = schedule_item.cached_combined_dimensions.get("paikkala", [""])
    if not room_slug:
        raise ValueError("paikkalize_schedule_item a schedule item that is not using Paikkala?!? Preposterous!!!")

    if reservation_start_str := schedule_item.cached_combined_annotations.get("paikkala:reservationStartsAt"):
        reservation_start = parse_datetime(reservation_start_str)
    elif settings.DEBUG:
        reservation_start = now()
    else:
        reservation_start = schedule_item.start_time.replace(hour=9, minute=0, tzinfo=tz)

    annotations = schedule_item.cached_combined_annotations
    numbered_seats = annotations.get("paikkala:haveNumberedSeats", True)
    max_per_user = annotations.get("paikkala:maxTicketsPerUser", meta.paikkala_default_max_tickets_per_user)
    max_per_batch = annotations.get("paikkala:maxTicketsPerBatch", meta.paikkala_default_max_tickets_per_batch)

    attrs = dict(
        event_name=schedule_item.event.name,
        name=truncatechars(schedule_item.title, PaikkalaProgram._meta.get_field("name").max_length),  # type: ignore
        require_user=True,
        reservation_start=reservation_start,
        reservation_end=schedule_item.cached_end_time,
        invalid_after=schedule_item.cached_end_time,
        automatic_max_tickets=True,
        max_tickets_per_user=max_per_user,
        max_tickets_per_batch=max_per_batch,
        numbered_seats=numbered_seats,
    )
    attrs.update(paikkalkwargs)

    paikkala_program = PaikkalaProgram.objects.filter(kompassi_v2_schedule_item=schedule_item).first()
    if paikkala_program:
        log_get_or_create(logger, paikkala_program, False)

        for k, v in attrs.items():
            setattr(paikkala_program, k, v)
        paikkala_program.save(update_fields=attrs.keys())

        return paikkala_program

    cache = meta.universe.preload_dimensions()
    paikkala_dimension_value = cache.values_by_dimension["paikkala"][room_slug]
    paikkala_room = paikkalize_room(schedule_item.event, paikkala_dimension_value)
    paikkala_program = PaikkalaProgram(room=paikkala_room, max_tickets=0, **attrs)
    paikkala_program.save()
    log_get_or_create(logger, paikkala_program, True)

    schedule_item.paikkala_program = paikkala_program
    schedule_item.paikkala_special_reservation_code = uuid4()
    schedule_item.save(update_fields=["paikkala_program", "paikkala_special_reservation_code"])

    paikkala_program.rows.set(PaikkalaRow.objects.filter(zone__room=paikkala_room))
    paikkala_program.full_clean()  # IMPORTANT: Populates max_tickets
    paikkala_program.save()

    return paikkala_program


def repaikkalize_event(event: Event):
    logger.info("Repaikkalizing event %s", event)
    meta = event.program_v2_event_meta
    if not meta:
        raise ValueError("Event is not using Program V2")

    schedule_items = meta.schedule_items.filter(cached_combined_dimensions__contains=dict(paikkala=[])).distinct()
    num_schedule_items = schedule_items.count()

    logger.info("There are %d schedule items using Paikkala", num_schedule_items)

    paikkala_programs = PaikkalaProgram.objects.filter(event_name=event.name)
    paikkala_rooms = PaikkalaRoom.objects.filter(program__in=paikkala_programs)
    paikkala_zones = PaikkalaZone.objects.filter(room__in=paikkala_rooms)
    paikkala_room_mappings = PaikkalaRoomMapping.objects.filter(
        paikkala_dimension_value__dimension__universe=meta.universe
    )

    logger.info("Clearing old Paikkala data")
    schedule_items.update(paikkala_program=None)
    paikkala_room_mappings.delete()
    paikkala_programs.delete()
    paikkala_zones.delete()
    paikkala_rooms.delete()

    # I am paranoid about runaway cascades
    schedule_items = meta.schedule_items.filter(cached_combined_dimensions__contains=dict(paikkala=[])).distinct()
    if schedule_items.count() != num_schedule_items:
        raise AssertionError("number of schedule items changed during repaikkalize")

    for schedule_item in schedule_items.all():
        logger.info("Repaikkalizing %s", schedule_item)
        paikkalize_schedule_item(schedule_item)

    if paikkala_programs.all().count() != num_schedule_items:
        raise AssertionError("number of paikkala programs does not match number of schedule items after repaikkalize")


def get_paikkala_special_reservation_url(schedule_item: ScheduleItem) -> str:
    return settings.KOMPASSI_BASE_URL + reverse(
        "program_v2:paikkala_special_reservation_view",
        args=[schedule_item.paikkala_special_reservation_code],
    )


PAIKKALA_ANNOTATION_DTOS = [
    AnnotationDTO(
        slug="paikkala:reservationStartsAt",
        type=AnnotationDataType.DATETIME,
        title=dict(
            fi="Varauksen alkamisaika (Paikkala)",
            en="Reservation start time (Paikkala)",
            sv="Början av reservation (Paikkala)",
        ),
    ),
    AnnotationDTO(
        slug="paikkala:isStartTimeDisplayed",
        type=AnnotationDataType.BOOLEAN,
        title=dict(
            fi="Alkuaika näkyvissä (Paikkala)",
            en="Start time is displayed (Paikkala)",
        ),
        # NOTE default=True
    ),
    AnnotationDTO(
        slug="paikkala:haveNumberedSeats",
        type=AnnotationDataType.BOOLEAN,
        title=dict(
            fi="Numeroidut paikat (Paikkala)",
            en="Numbered seats (Paikkala)",
        ),
        # NOTE default=True
    ),
    AnnotationDTO(
        slug="paikkala:maxTicketsPerBatch",
        type=AnnotationDataType.NUMBER,
        title=dict(
            fi="Maksimimäärä lippuja per varaus (Paikkala)",
            en="Maximum number of tickets per reservation (Paikkala)",
        ),
    ),
    AnnotationDTO(
        slug="paikkala:maxTicketsPerUser",
        type=AnnotationDataType.NUMBER,
        title=dict(
            fi="Maksimimäärä lippuja per käyttäjä (Paikkala)",
            en="Maximum number of tickets per user (Paikkala)",
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


class FakeRow(pydantic.BaseModel):
    name: str = "1"


class FakeTicket(pydantic.BaseModel, arbitrary_types_allowed=True):
    program: PaikkalaProgram
    row: FakeRow
    zone: PaikkalaZone | None
    number: str = "Numeroimaton"

    @classmethod
    def for_paikkala_program(cls, program: PaikkalaProgram) -> Self:
        # HACK: Tampere Hall (Tracon/Tampere kuplii) colour code entrances
        # This needs to be a zone that has row number 1
        # Main Auditorium: eg. Etupermanto vasen
        # Small Auditorium: prefer Permanto vasen
        zone = program.zones.filter(name__contains="ermanto vasen").order_by("id").first()
        return cls(program=program, row=FakeRow(), zone=zone)
