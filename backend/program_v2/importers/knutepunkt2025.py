import logging
from datetime import datetime, timedelta
from functools import cached_property
from uuid import UUID
from zoneinfo import ZoneInfo

import pydantic
import requests

from core.models.event import Event
from core.models.organization import Organization
from core.models.venue import Venue
from core.utils.log_utils import log_get_or_create
from core.utils.model_utils import slugify
from dimensions.models.value_ordering import ValueOrdering
from graphql_api.language import SUPPORTED_LANGUAGE_CODES
from program_v2.models.dimension_dto import DimensionDTO, DimensionValueDTO
from program_v2.models.meta import ProgramV2EventMeta

from ..consts import (
    DATE_DIMENSION_TITLE_LOCALIZED,
    WEEKDAYS_LOCALIZED,
)
from ..models.program import Program
from ..models.schedule import ScheduleItem

logger = logging.getLogger("kompassi")
TZ = ZoneInfo("Europe/Oslo")
DATE_CUTOFF = timedelta(hours=4)
KP_EVENT_ID = UUID("07871e21-12e4-447e-8edf-652670727321")

PROGRAM_TYPE_TITLES = {
    1: "Larp",
    2: "Talk",
    3: "Roundtable",
    4: "Panel",
    5: "Workshop",
    6: "Other",
    7: "Food",
    11: "Show",
    12: "Dancefloor",
    13: "Singalong",
    14: "Party",
    15: "Mingle",
}
TRACK_TITLES = {
    1: "The Unexpected",
    2: "Leveling Up Larping",
    3: "Community",
    4: "Larping for Good",
    5: "Making It Work",
    6: "Designing the Story",
    7: "Social",
}


class Location(pydantic.BaseModel):
    id: UUID
    name: str

    @classmethod
    def get_all(cls):
        response = requests.get("https://kp2025api.azurewebsites.net/api/Locations")
        response.raise_for_status()
        return [cls.model_validate(obj) for obj in response.json()]


class ProgramItem(pydantic.BaseModel):
    id: UUID
    title: str
    tagline: str
    track_id: int | None = pydantic.Field(validation_alias="trackId", default=None)
    program_type_id: int = pydantic.Field(validation_alias="programTypeId")
    description: str = pydantic.Field(validation_alias="content", repr=False)
    location_id: UUID = pydantic.Field(validation_alias="locationId")
    is_cancelled: bool = pydantic.Field(validation_alias="isCancelled")
    raw_start_time: str = pydantic.Field(validation_alias="startTime")
    raw_end_time: str = pydantic.Field(validation_alias="endTime")
    event_id: UUID = pydantic.Field(validation_alias="eventId")

    @classmethod
    def get_all(cls):
        response = requests.get("https://kp2025api.azurewebsites.net/api/ProgramItems")
        response.raise_for_status()
        return [cls.model_validate(obj) for obj in response.json()]

    @property
    def start_time(self):
        return datetime.strptime(self.raw_start_time, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=TZ)

    @property
    def end_time(self):
        return datetime.strptime(self.raw_end_time, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=TZ)

    @property
    def length(self):
        return self.end_time - self.start_time

    @cached_property
    def date(self):
        return (self.start_time - DATE_CUTOFF).date()


def import_knutepunkt(event_slug: str):
    kp_programs = ProgramItem.get_all()
    locations_by_id = {location.id: location for location in Location.get_all()}
    program_type_ids = {kp_program.program_type_id for kp_program in kp_programs}
    track_ids = {kp_program.track_id for kp_program in kp_programs if kp_program.track_id}
    dates = {kp_program.date.isoformat(): kp_program.date for kp_program in kp_programs}

    organization, created = Organization.objects.get_or_create(
        slug="knutepunkt",
        defaults=dict(
            name="Knutepunkt organizers",
            name_genitive="Knutepunkt organizers",
        ),
    )
    log_get_or_create(logger, organization, created)

    venue, created = Venue.objects.get_or_create(
        name="Quality Hotel Entry (Oslo)",
        defaults=dict(
            name_inessive="Quality Hotel Entry (Oslo)",
        ),
    )
    log_get_or_create(logger, venue, created)

    event, created = Event.objects.get_or_create(
        slug=event_slug,
        defaults=dict(
            name="Knutepunkt 2025",
            organization=organization,
            venue=venue,
            start_time=datetime(2025, 3, 13, 15, 0, tzinfo=TZ),
            end_time=datetime(2025, 3, 13, 15, 0, tzinfo=TZ),
            public=False,
            homepage_url="https://knutepunkt.org",
        ),
    )
    log_get_or_create(logger, event, created)

    (_, _, _, _, location_dimension) = DimensionDTO.save_many(
        event,
        [
            DimensionDTO(
                slug="date",
                title=DATE_DIMENSION_TITLE_LOCALIZED,
                value_ordering=ValueOrdering.SLUG,
                choices=[
                    DimensionValueDTO(
                        slug=date.isoformat(),
                        title={
                            language: WEEKDAYS_LOCALIZED[language][date.weekday()]
                            for language in SUPPORTED_LANGUAGE_CODES
                        },
                    )
                    for date in dates.values()
                ],
            ),
            DimensionDTO(
                slug="event",
                title={"en": "Event"},
                choices=[
                    DimensionValueDTO(
                        slug="aweek",
                        title={"en": "A Week in Norway"},
                    ),
                    DimensionValueDTO(
                        slug="knutepunkt",
                        title={"en": "Knutepunkt"},
                    ),
                ],
            ),
            DimensionDTO(
                slug="type",
                title={"en": "Program type"},
                value_ordering=ValueOrdering.MANUAL,
                choices=[
                    DimensionValueDTO(
                        slug=slugify(title),
                        title={"en": title},
                    )
                    for program_type_id in program_type_ids
                    if (title := PROGRAM_TYPE_TITLES.get(program_type_id))
                ],
            ),
            DimensionDTO(
                slug="track",
                title={"en": "Track"},
                value_ordering=ValueOrdering.MANUAL,
                choices=[
                    DimensionValueDTO(
                        slug=slugify(title),
                        title={"en": title},
                    )
                    for track_id in track_ids
                    if (title := TRACK_TITLES.get(track_id))
                ],
            ),
            DimensionDTO(
                slug="location",
                title={"en": "Location"},
                choices=[
                    DimensionValueDTO(
                        slug=str(location.id),
                        title={"en": location.name},
                    )
                    for location in locations_by_id.values()
                ],
            ),
        ],
    )

    (admin_group,) = ProgramV2EventMeta.get_or_create_groups(event, ["admins"])
    ProgramV2EventMeta.objects.update_or_create(
        event=event,
        defaults=dict(
            admin_group=admin_group,
            location_dimension=location_dimension,
            is_accepting_feedback=False,
        ),
    )

    Program.objects.filter(event=event).delete()
    programs = Program.objects.bulk_create(
        Program(
            slug=str(kp_program.id),
            event=event,
            title=kp_program.title,
            description=kp_program.description,
            annotations={"knutepunkt:tagline": kp_program.tagline},
        )
        for kp_program in kp_programs
        if not kp_program.is_cancelled
    )

    ScheduleItem.objects.bulk_create(
        ScheduleItem(
            slug=str(kp_program.id),
            program=program,
            start_time=kp_program.start_time,
            length=kp_program.length,
        ).with_generated_fields()
        for program, kp_program in zip(programs, kp_programs, strict=True)
    )

    for program, kp_program in zip(programs, kp_programs, strict=True):
        program.set_dimension_values(
            dict(
                date=[kp_program.date.isoformat()],
                event=["knutepunkt"] if kp_program.event_id == KP_EVENT_ID else ["aweek"],
                location=[str(locations_by_id[kp_program.location_id].id)],
                type=[slugify(PROGRAM_TYPE_TITLES[kp_program.program_type_id])],
                track=[slugify(TRACK_TITLES[kp_program.track_id])] if kp_program.track_id else [],
            )
        )

    Program.refresh_cached_fields_qs(Program.objects.filter(event=event))
