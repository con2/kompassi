from __future__ import annotations

import logging
from collections.abc import Collection, Mapping
from datetime import tzinfo
from functools import cached_property
from typing import TYPE_CHECKING, Any, Self

from django.conf import settings
from django.db import models, transaction
from django.http import HttpRequest
from django.urls import reverse
from django.utils.timezone import now

from core.models import Event
from core.utils.model_utils import slugify, validate_slug
from dimensions.models.scope import Scope
from dimensions.utils.dimension_cache import DimensionCache
from forms.models.response import Response
from forms.models.survey import Survey
from graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, getattr_message_in_language
from involvement.models.enums import InvolvementType
from involvement.models.invitation import Invitation
from involvement.models.involvement import Involvement

from .annotations import extract_annotations

if TYPE_CHECKING:
    from .meta import ProgramV2EventMeta
    from .program_dimension_value import ProgramDimensionValue
    from .schedule import ScheduleItem


logger = logging.getLogger("kompassi")


class Program(models.Model):
    id: int

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="programs")
    title = models.CharField(max_length=1023)
    slug = models.CharField(max_length=1023, validators=[validate_slug])
    description = models.TextField(blank=True)
    annotations = models.JSONField(blank=True, default=dict)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # denormalized fields
    cached_dimensions = models.JSONField(default=dict, blank=True)
    cached_earliest_start_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "The earliest start time of any schedule item of this program. "
            "NOTE: This is not the same as the program's start time. "
            "The intended purpose of this field is to exclude programs that have not yet started. "
            "Always use `scheduleItems` for the purpose of displaying program times."
        ),
    )
    cached_latest_end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "The latest end time of any schedule item of this program. "
            "NOTE: This is not the same as the program's start end. "
            "The intended purpose of this field is to exclude programs that have already ended. "
            "Always use `scheduleItems` for the purpose of displaying program times."
        ),
    )
    cached_location = models.JSONField(blank=True, default=dict)
    cached_color = models.CharField(max_length=15, blank=True, default="")

    program_offer = models.ForeignKey(
        Response,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="programs",
        help_text="If this program was created from a program offer, this field will be set to the program offer.",
    )

    # TODO(#665)
    is_cancelled = False

    @property
    def is_active(self) -> bool:
        return not self.is_cancelled

    # related fields
    dimensions: models.QuerySet[ProgramDimensionValue]
    involvements: models.QuerySet[Involvement]
    schedule_items: models.QuerySet[ScheduleItem]
    event_id: int

    class Meta:
        unique_together = ("event", "slug")

    def __str__(self):
        return str(self.title)

    def refresh_cached_fields(self):
        self.refresh_cached_dimensions()
        self.refresh_cached_times()

    @classmethod
    def refresh_cached_fields_qs(cls, queryset: models.QuerySet[Self]):
        cls.refresh_cached_dimensions_qs(queryset)
        cls.refresh_cached_times_qs(queryset)

    def _build_dimensions(self):
        """
        Used to populate cached_dimensions
        """
        # TODO should all event dimensions always be present, or only those with values?
        dimensions = {dimension.slug: [] for dimension in self.event.program_universe.dimensions.all()}
        for pdv in self.dimensions.all():
            dimensions[pdv.value.dimension.slug].append(pdv.value.slug)
        return dimensions

    def _build_location(self):
        localized_locations: dict[str, set[str]] = {}

        for pdv in self.dimensions.filter(value__dimension__slug="room").distinct():
            for lang in SUPPORTED_LANGUAGES:
                title = getattr_message_in_language(pdv.value, "title", lang.code)
                if not title:
                    # placate typechecker
                    continue

                localized_locations.setdefault(lang.code, set()).add(title)

        # if both "foo" and "foo, bar" are present, only "foo, bar" is included
        for locations in localized_locations.values():
            for location in list(locations):
                for other_location in list(locations):
                    if location != other_location and location in other_location and location in locations:
                        locations.remove(location)

        return {lang: ", ".join(locations) for lang, locations in localized_locations.items() if locations}

    def _get_color(self):
        """
        Gets a color for the program from its dimension values.
        TODO deterministic behaviour when multiple colors are present (ordering for dimensions/values?)
        """
        first_pdv_with_color = self.dimensions.exclude(value__color="").first()
        return first_pdv_with_color.value.color if first_pdv_with_color else ""

    def refresh_cached_dimensions(self):
        from .schedule import ScheduleItem

        self.cached_dimensions = self._build_dimensions()
        self.cached_location = self._build_location()
        self.cached_color = self._get_color()
        self.save(update_fields=["cached_dimensions", "cached_location", "cached_color", "updated_at"])
        self.schedule_items.update(cached_location=self.cached_location)

        bulk_update_schedule_items = []
        for schedule_item in self.schedule_items.filter(program=self).select_for_update(of=("self",)):
            schedule_item.cached_location = self.cached_location
            bulk_update_schedule_items.append(schedule_item)
        ScheduleItem.objects.bulk_update(bulk_update_schedule_items, ["cached_location"])

    program_batch_size = 100
    schedule_item_batch_size = 100

    @classmethod
    def refresh_cached_dimensions_qs(cls, queryset: models.QuerySet[Self]):
        from .schedule import ScheduleItem

        with transaction.atomic():
            bulk_update_programs = []
            for program in queryset.select_for_update(of=("self",)).only(
                "id",
                "cached_dimensions",
                "cached_location",
                "cached_color",
            ):
                program.cached_dimensions = program._build_dimensions()
                program.cached_location = program._build_location()
                program.cached_color = program._get_color()
                bulk_update_programs.append(program)
            num_programs_updated = cls.objects.bulk_update(
                bulk_update_programs,
                ["cached_dimensions", "cached_location", "cached_color"],
                batch_size=cls.program_batch_size,
            )
            logger.info("Refreshed cached dimensions for %s programs", num_programs_updated)

            bulk_update_schedule_items = []
            for schedule_item in (
                ScheduleItem.objects.filter(program__in=queryset)
                .select_for_update(of=("self",))
                .select_related("program")
                .only("program__cached_location")
            ):
                schedule_item.cached_location = schedule_item.program.cached_location
                bulk_update_schedule_items.append(schedule_item)
            num_schedule_items_updated = ScheduleItem.objects.bulk_update(
                bulk_update_schedule_items,
                ["cached_location"],
                batch_size=cls.schedule_item_batch_size,
            )
            logger.info("Refreshed cached locations for %s schedule items", num_schedule_items_updated)

    def refresh_cached_times(self):
        """
        Used to populate cached_earliest_start_time and cached_latest_end_time
        """
        earliest_start_time = self.schedule_items.order_by("start_time").first()
        latest_end_time = self.schedule_items.order_by("cached_end_time").last()

        self.cached_earliest_start_time = earliest_start_time.start_time if earliest_start_time else None
        self.cached_latest_end_time = latest_end_time.cached_end_time if latest_end_time else None

        self.save(update_fields=["cached_earliest_start_time", "cached_latest_end_time", "updated_at"])

    @classmethod
    def refresh_cached_times_qs(cls, queryset: models.QuerySet[Self]):
        with transaction.atomic():
            bulk_update = []
            for program in queryset.select_for_update(of=("self",)).only(
                "id",
                "cached_earliest_start_time",
                "cached_latest_end_time",
            ):
                earliest_start_time = program.schedule_items.order_by("start_time").first()
                latest_end_time = program.schedule_items.order_by("cached_end_time").last()

                program.cached_earliest_start_time = earliest_start_time.start_time if earliest_start_time else None
                program.cached_latest_end_time = latest_end_time.cached_end_time if latest_end_time else None

                bulk_update.append(program)
            num_updated = cls.objects.bulk_update(
                bulk_update,
                ["cached_earliest_start_time", "cached_latest_end_time"],
                batch_size=cls.program_batch_size,
            )
            logger.info("Refreshed cached times for %s programs", num_updated)

    @cached_property
    def meta(self) -> ProgramV2EventMeta:
        if (meta := self.event.program_v2_event_meta) is None:
            raise TypeError(f"Event {self.event.slug} does not have program_v2_event_meta but Programs are present")

        return meta

    @cached_property
    def timezone(self) -> tzinfo:
        return self.event.timezone

    def get_calendar_export_link(self, request: HttpRequest):
        return request.build_absolute_uri(
            reverse(
                "program_v2:single_program_calendar_export_view",
                kwargs=dict(
                    event_slug=self.event.slug,
                    program_slug=self.slug,
                ),
            )
        )

    @property
    def is_accepting_feedback(self) -> bool:
        return bool(
            self.meta.is_accepting_feedback
            and self.cached_earliest_start_time
            and now() >= self.cached_earliest_start_time
        )

    @property
    def scope(self) -> Scope:
        return self.event.scope

    # TODO Automatic dimensions
    # TODO Automatic annotations

    @transaction.atomic
    def set_dimension_values(self, values_to_set: Mapping[str, Collection[str]], cache: DimensionCache):
        """
        Changes only those dimension values that are present in dimension_values.

        NOTE: Caller must call refresh_cached_dimensions() or refresh_cached_dimensions_qs()
        afterwards to update the cached_dimensions field.

        :param values_to_set: Mapping of dimension slug to list of value slugs.
        :param cache: Cache from Universe.preload_dimensions()
        """
        from .program_dimension_value import ProgramDimensionValue

        bulk_delete = self.dimensions.filter(value__dimension__slug__in=values_to_set.keys())
        bulk_create: list[ProgramDimensionValue] = []

        for dimension_slug, value_slugs in values_to_set.items():
            bulk_delete = bulk_delete.exclude(
                value__dimension__slug=dimension_slug,
                value__slug__in=value_slugs,
            )

            for value_slug in value_slugs:
                if value_slug not in self.cached_dimensions.get(dimension_slug, []):
                    bulk_create.append(
                        ProgramDimensionValue(
                            program=self,
                            value=cache.values_by_dimension[dimension_slug][value_slug],
                        )
                    )

        bulk_delete.delete()
        ProgramDimensionValue.objects.bulk_create(bulk_create)

    @classmethod
    def from_program_offer(
        cls,
        program_offer: Response,
        slug: str = "",
        title: str = "",
        created_by: Any | None = None,  # User
        dimension_values: Mapping[str, Collection[str]] | None = None,
    ) -> Self:
        """
        Accept a program offer and return the new Program instance.
        """
        event = program_offer.event
        cache = event.program_universe.preload_dimensions()

        combined_dimension_values: Mapping[str, Collection[str]] = dict(program_offer.survey.cached_default_dimensions)
        combined_dimension_values.update(program_offer.cached_dimensions)
        if dimension_values is not None:
            combined_dimension_values.update(dimension_values)
        combined_dimension_values.update(
            state=["accepted"],
        )

        values, warnings = program_offer.get_processed_form_data()
        if warnings:
            logger.warning("Program offer %s had form data warnings: %s", program_offer.id, warnings)

        annotations = extract_annotations(values)

        if not title:
            title = values.get("title", "")

        if not slug:
            slug = slugify(title)

        program = cls(
            event=program_offer.event,
            slug=slug,
            title=title,
            description=values.get("description", ""),
            annotations=annotations,
            created_by=created_by,
            cached_dimensions={},
            program_offer=program_offer,
        )
        program.full_clean()
        program.save()
        program.set_dimension_values(combined_dimension_values, cache=cache)
        program.refresh_cached_fields()

        program_offer.set_dimension_values(program.cached_dimensions, cache=cache)
        program_offer.refresh_cached_fields()

        Involvement.from_accepted_program_offer(
            program_offer,
            program,
            cache=event.involvement_universe.preload_dimensions(),
        )

        return program

    @property
    def program_hosts(self) -> models.QuerySet[Involvement]:
        return (
            Involvement.objects.filter(
                program=self,
                is_active=True,
            )
            .select_related(
                "person",
                "program",
            )
            .order_by(
                "person__surname",
                "person__first_name",
                "program__cached_first_start_time",
            )
        )

    def invite_program_host(
        self,
        email: str,
        survey: Survey,
        language: str = DEFAULT_LANGUAGE,
        created_by: Any | None = None,  # User
    ) -> Invitation:
        if survey.involvement_type != InvolvementType.PROGRAM_HOST:
            raise ValueError(f"Survey {survey} cannot be used to invite program hosts")

        invitation = Invitation(
            survey=survey,
            program=self,
            email=email,
            created_by=created_by,
            language=language,
        )
        invitation.full_clean()
        invitation.save()
        invitation.send()

        return invitation

    @property
    def invitations(self) -> models.QuerySet[Invitation]:
        return (
            Invitation.objects.filter(
                program=self,
                used_at__isnull=True,
            )
            .select_related(
                "survey",
                "program",
            )
            .order_by("created_at")
        )
