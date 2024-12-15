import logging
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from django.db.models import QuerySet
from django.utils.timezone import get_current_timezone

from core.models import Event
from dimensions.models.dimension import Dimension
from dimensions.models.value_ordering import ValueOrdering
from programme.models.category import Category
from programme.models.programme import Programme
from programme.models.room import Room
from programme.models.tag import Tag

from ..consts import (
    CATEGORY_DIMENSION_TITLE_LOCALIZED,
    DATE_DIMENSION_TITLE_LOCALIZED,
    DEFAULT_COLORS,
    ROOM_DIMENSION_TITLE_LOCALIZED,
    TAG_DIMENSION_TITLE_LOCALIZED,
    WEEKDAYS_LOCALIZED,
)
from ..models.annotations import ANNOTATIONS
from ..models.dimension_dto import DimensionDTO, DimensionValueDTO
from ..models.dimension_values import ProgramDimensionValue
from ..models.program import Program
from ..models.schedule import ScheduleItem

logger = logging.getLogger("kompassi")
tz = get_current_timezone()


@dataclass
class DefaultImporter:
    """
    The default importer for Kompassi V1 program items.
    Subclass this to implement custom import logic.
    The methods you usually want to reimplement are `get_program_dimension_values` and `build_dimensions`.
    If you need to change the way programs are imported, you can reimplement `get_program`, `get_schedule_items`, `get_length`, `get_start_time`, and `get_end_time`.
    If you are thinking you need to reimplement `import_program`, there are probably dragons.
    """

    event: Event
    language: str = "fi"

    date_cutoff_time = timedelta(hours=4)  # 04:00 local time

    def get_date_dimension_value(self, programme: Programme) -> list[str]:
        """
        Return the date dimension value for the programme.

        The `date_cutoff_time` is used to determine at which time of the night the date changes.
        Use this to make the wee hours of the night belong to the previous day.
        """
        if not programme.start_time:
            raise ValueError(f"Programme {programme} has no start time")

        return [(programme.start_time.astimezone(tz) - self.date_cutoff_time).date().isoformat()]

    def _get_date_dimension_values(self) -> Iterable[DimensionValueDTO]:
        """
        Return a list of DimensionValueDTOs for the date dimension.
        """
        if not self.event.start_time:
            raise ValueError(f"Event {self.event} has no start time")
        if not self.event.end_time:
            raise ValueError(f"Event {self.event} has no end time")

        cur_date = self.event.start_time.astimezone(tz).date()
        end_date = self.event.end_time.astimezone(tz).date()

        while cur_date <= end_date:
            yield DimensionValueDTO(
                slug=cur_date.isoformat(),
                title={self.language: WEEKDAYS_LOCALIZED[self.language][cur_date.weekday()]},
            )
            cur_date += timedelta(days=1)

    def _get_date_dimension(self) -> DimensionDTO:
        """
        Reusable date dimension for importers that define their own dimensions in `get_dimensions`.
        """
        return DimensionDTO(
            slug="date",
            title=DATE_DIMENSION_TITLE_LOCALIZED,
            choices=list(self._get_date_dimension_values()),
            value_ordering=ValueOrdering.SLUG,
        )

    def _get_room_dimension_values(self) -> Iterable[DimensionValueDTO]:
        return [
            DimensionValueDTO(slug=room.slug, title={self.language: room.name})
            for room in Room.objects.filter(
                event=self.event,
                programmes__state="published",
                programmes__start_time__isnull=False,
                programmes__length__isnull=False,
            ).distinct()
        ]

    def _get_room_dimension(self) -> DimensionDTO:
        return DimensionDTO(
            slug="room",
            title=ROOM_DIMENSION_TITLE_LOCALIZED,
            choices=list(self._get_room_dimension_values()),
        )

    def get_dimensions(self) -> list[DimensionDTO]:
        """
        Return a list of DimensionDTOs for the event.
        Don't call `DimensionDTO.save_many` on them, as this method is called by the importer.
        """
        return [
            self._get_date_dimension(),
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
            DimensionDTO(
                slug="tag",
                title=TAG_DIMENSION_TITLE_LOCALIZED,
                choices=[
                    DimensionValueDTO(slug=tag.slug, title={self.language: tag.title})
                    for tag in Tag.objects.filter(event=self.event)
                ],
            ),
            self._get_room_dimension(),
        ]

    def get_program_dimension_values(self, programme: Programme) -> dict[str, list[str]]:
        values: dict[str, set[str]] = dict(date=set(self.get_date_dimension_value(programme)))

        for value_source in [
            programme.category,
            programme.room,
            programme.form_used,
            *programme.tags.all(),
        ]:
            if value_source:
                for dimension_slug, value_slugs in value_source.v2_dimensions.items():
                    values.setdefault(dimension_slug, set()).update(value_slugs)

        return {k: list(v) for k, v in values.items()}

    def get_length(self, programme: Programme) -> timedelta:
        """
        Return the length of the programme in minutes.
        """
        if not programme.length:
            raise ValueError(f"Programme {programme} has no length")

        return timedelta(minutes=programme.length)

    def get_start_time(self, programme: Programme) -> datetime:
        """
        Return the start time of the programme.
        """
        if not programme.start_time:
            raise ValueError(f"Programme {programme} has no start time")

        return programme.start_time

    def get_end_time(self, programme: Programme) -> datetime:
        """
        Return the end time of the programme.
        """
        return self.get_start_time(programme) + self.get_length(programme)

    program_unique_fields = ("event", "slug")
    program_update_fields = ("title", "description", "annotations", "updated_at")

    def get_program_annotations(self, programme: Programme) -> dict[str, Any]:
        annotations = {}
        for annotation in ANNOTATIONS:
            if extract_value := annotation.from_v1_programme:
                value = extract_value(programme)
                if value not in (None, ""):
                    annotations[annotation.slug] = value
        return annotations

    def get_program(self, programme: Programme) -> Program:
        """
        Return an unsaved V2 Program instance for the V1 Programme.
        NOTE: If you add other fields not listed here, remember to add them to `program_update_fields`.
        """
        return Program(
            event=programme.category.event,
            slug=programme.slug,
            title_fi=programme.title,
            description_fi=programme.description,
            annotations=self.get_program_annotations(programme),
        )

    def get_schedule_items(self, v1_programme: Programme, v2_program: Program) -> list[ScheduleItem]:
        """
        Return a list of unsaved V2 ScheduleItems for the V1 Programme.
        """
        return [
            ScheduleItem(
                program=v2_program,
                start_time=self.get_start_time(v1_programme),
                length=self.get_length(v1_programme),
            ).with_generated_fields()
        ]

    def get_eligible_programmes(self, queryset: QuerySet[Programme]) -> QuerySet[Programme]:
        return queryset.filter(
            state="published",
            start_time__isnull=False,
            length__isnull=False,
            category__public=True,
        ).order_by("id")

    program_batch_size = 100
    schedule_item_batch_size = 100
    pdv_batch_size = 400

    def import_dimensions(
        self,
        clear: bool = False,
        refresh_cached_dimensions: bool = True,
    ) -> list[Dimension]:
        logger.info("Starting dimensions import for %s", self.event.slug)
        meta = self.event.program_v2_event_meta
        universe = self.event.program_universe

        location_dimension_slug = ""

        if clear:
            # we have to replace the location and primary dimensions with their new versions
            if meta:
                update_fields = []
                if meta.location_dimension:
                    location_dimension_slug = meta.location_dimension.slug
                    meta.location_dimension = None
                    update_fields.append("location_dimension")
                if update_fields:
                    meta.save(update_fields=update_fields)

            _, deleted = universe.dimensions.all().delete()
            logger.info("Dimension clearing deleted %s", deleted or "nothing")

        dimension_dtos = self.get_dimensions()
        dimensions = DimensionDTO.save_many(self.event, dimension_dtos, refresh_cached=False)
        logger.info("Imported %d dimensions for %s", len(dimension_dtos), self.event.slug)

        if clear and meta:
            update_fields = []
            # XXX pyrekt are you drunk? (type: ignores)
            if location_dimension_slug:
                meta.location_dimension = Dimension.objects.get(  # type: ignore
                    event=self.event,
                    slug=location_dimension_slug,
                )
                update_fields.append("location_dimension")
            if update_fields:
                meta.save(update_fields=update_fields)

        if refresh_cached_dimensions:
            Program.refresh_cached_dimensions_qs(self.event.programs.all())

        return dimensions

    def import_program(
        self,
        queryset: QuerySet[Programme],
        clear: bool = False,
        refresh_cached_fields: bool = True,
    ) -> list[Program]:
        logger.info("Starting program import for %s", self.event.slug)

        eligible_queryset = self.get_eligible_programmes(queryset)

        if clear:
            _, deleted = Program.objects.filter(event=self.event).delete()
            logger.info("Program clearing deleted %s", deleted or "nothing")
        else:
            # remove programs that have since been un-published
            _, deleted = (
                Program.objects.filter(
                    event=self.event,
                    slug__in=queryset.values_list("slug", flat=True),
                )
                .exclude(
                    slug__in=eligible_queryset.values_list("slug", flat=True),
                )
                .delete()
            )
            logger.info("Un-published program cleanup deleted %s", deleted or "nothing")

        v1_programmes = list(eligible_queryset)

        v2_programs = Program.objects.bulk_create(
            (self.get_program(programme) for programme in v1_programmes),
            update_conflicts=True,
            unique_fields=self.program_unique_fields,
            update_fields=self.program_update_fields,
            batch_size=self.program_batch_size,
        )

        logger.info("Imported %d programs for %s", len(v2_programs), self.event.slug)

        # cannot use ScheduleItem.objects.bulk_create(…, update_conflicts=True)
        # because there is no unique constraint
        ScheduleItem.objects.filter(program__in=v2_programs).delete()
        schedule_upsert = (
            schedule_item
            for v1_programme, v2_program in zip(v1_programmes, v2_programs, strict=True)
            for schedule_item in self.get_schedule_items(v1_programme, v2_program)
            if v1_programme.start_time is not None and v1_programme.length is not None
        )
        schedule_item_ids = [
            schedule_item.id
            for schedule_item in ScheduleItem.objects.bulk_create(
                schedule_upsert,
                batch_size=self.schedule_item_batch_size,
            )
        ]
        logger.info("Imported %d schedule items for %s", len(schedule_item_ids), self.event.slug)

        _, deleted = ScheduleItem.objects.filter(program__in=v2_programs).exclude(id__in=schedule_item_ids).delete()
        logger.info("Schedule item cleanup deleted %s", deleted or "nothing")

        upsert_cache = ProgramDimensionValue.build_upsert_cache(self.event)
        pdv_upserts = (
            item
            for programme, program_v2 in zip(v1_programmes, v2_programs, strict=True)
            for item in ProgramDimensionValue.build_upsertables(
                program_v2,
                self.get_program_dimension_values(programme),
                upsert_cache,
            )
        )
        pdv_ids = [pdv.id for pdv in ProgramDimensionValue.bulk_upsert(pdv_upserts, batch_size=self.pdv_batch_size)]
        logger.info("Imported %d program dimension values", len(pdv_ids))

        # delete program dimension values that are not set in the new data
        _, deleted = ProgramDimensionValue.objects.filter(program__in=v2_programs).exclude(id__in=pdv_ids).delete()
        logger.info("Stale PDV cleanup deleted %s", deleted or "nothing")

        if refresh_cached_fields:
            Program.refresh_cached_fields_qs(self.event.programs.all())

        logger.info("Finished program import for %s", self.event.slug)

        return v2_programs
