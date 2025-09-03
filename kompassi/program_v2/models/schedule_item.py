from __future__ import annotations

import logging
from collections.abc import Collection, Mapping
from datetime import datetime, timedelta, tzinfo
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, Self

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models, transaction
from django.utils.translation import get_language

from kompassi.core.models.event import Event
from kompassi.core.utils.locale_utils import get_message_in_language
from kompassi.core.utils.model_utils import make_slug_field, slugify
from kompassi.dimensions.models.dimension_value import DimensionValue
from kompassi.dimensions.models.scope import Scope
from kompassi.dimensions.models.universe import Universe
from kompassi.dimensions.utils.build_cached_dimensions import build_cached_dimensions
from kompassi.dimensions.utils.dimension_cache import DimensionCache
from kompassi.dimensions.utils.set_dimension_values import set_dimension_values
from kompassi.graphql_api.language import SUPPORTED_LANGUAGE_CODES

from .program import Program

if TYPE_CHECKING:
    from paikkala.models.programs import Program as PaikkalaProgram

    from .schedule_item_dimension_value import ScheduleItemDimensionValue

logger = logging.getLogger(__name__)


class ScheduleItem(models.Model):
    id: int

    slug = make_slug_field(
        unique=False,
        help_text=("NOTE: Slug must be unique within Event. It does not suffice to be unique within Program."),
    )
    program: models.ForeignKey[Program] = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="schedule_items",
    )

    start_time: datetime = models.DateTimeField()  # type: ignore
    duration: timedelta = models.DurationField()  # type: ignore

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # denormalized fields
    cached_end_time = models.DateTimeField()
    cached_event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        related_name="schedule_items",
    )
    cached_dimensions = models.JSONField(blank=True, default=dict)
    cached_combined_dimensions = models.JSONField(blank=True, default=dict)

    # TODO internal:formattedLocation:fi etc. annotations?
    cached_location = models.JSONField(blank=True, default=dict)

    annotations = models.JSONField(blank=True, default=dict)
    cached_combined_annotations = models.JSONField(blank=True, default=dict)  # lol precalc

    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="favorite_schedule_items", blank=True)

    paikkala_program: models.OneToOneField[PaikkalaProgram] | None = models.OneToOneField(
        "paikkala.Program",
        on_delete=models.SET_NULL,
        null=True,
        related_name="kompassi_v2_schedule_item",
    )
    paikkala_program_id: int | None

    # actual field instead of annotation because it is used to find the ScheduleItem
    # in the special reservation view
    paikkala_special_reservation_code = models.UUIDField(null=True, unique=True)

    dimensions: models.QuerySet[ScheduleItemDimensionValue]

    class Meta:
        ordering = ["cached_event", "start_time"]
        unique_together = [("cached_event", "slug")]
        indexes = [
            GinIndex(
                fields=["cached_combined_dimensions"],
                name="program_v2_scheduleitem_gin",
                opclasses=["jsonb_path_ops"],
            ),
        ]

    def __str__(self):
        scope_slug = self.scope.slug if self.scope else "None"
        return f"{scope_slug}/{self.slug}"

    @property
    def scope(self) -> Scope:
        return self.program.scope

    @property
    def event(self) -> Event:
        return self.program.event

    @property
    def universe(self) -> Universe:
        return self.program.event.program_universe

    @property
    def title(self):
        if subtitle := self.annotations.get("internal:subtitle", ""):
            return f"{self.program.title} – {subtitle}"
        else:
            return self.program.title

    @property
    def subtitle(self) -> str:
        return self.annotations.get("internal:subtitle", "")

    @subtitle.setter
    def subtitle(self, value: str):
        if value:
            self.annotations["internal:subtitle"] = value
        else:
            self.annotations.pop("internal:subtitle", None)

    @property
    def freeform_location(self) -> str:
        return self.annotations.get("internal:freeformLocation", "")

    @freeform_location.setter
    def freeform_location(self, value: str):
        if value:
            self.annotations["internal:freeformLocation"] = value
        else:
            self.annotations.pop("internal:freeformLocation", None)

    @property
    def _effective_annotations(self):
        """
        For use by resolve_cached_annotations, to allow treating Program and ScheduleItem the same.
        Other users should usually query .annotations directly.
        """
        return self.cached_combined_annotations

    @cached_property
    def timezone(self):
        return self.cached_event.timezone

    def _make_slug(self):
        if subtitle := self.annotations.get("internal:subtitle", ""):
            return f"{self.program.slug}-{slugify(subtitle)}"
        else:
            return self.program.slug

    @property
    def room_dimension_value(self) -> DimensionValue | None:
        from .schedule_item_dimension_value import ScheduleItemDimensionValue

        try:
            return self.dimensions.filter(value__dimension__slug="room").get().value
        except ScheduleItemDimensionValue.DoesNotExist:
            return None
        except ScheduleItemDimensionValue.MultipleObjectsReturned as e:
            raise ValueError("Multiple room dimension values found for schedule item %s", self) from e

    def _make_location(self) -> dict[str, str]:
        room_dimension_value = self.room_dimension_value
        freeform_location: str = self.annotations.get("internal:freeformLocation", "")

        if room_dimension_value and freeform_location:
            return {
                lang: f"{room_name} ({freeform_location})"
                for (lang, room_name) in room_dimension_value.title_dict.items()
            }
        elif room_dimension_value:
            return room_dimension_value.title_dict
        else:
            return dict.fromkeys(SUPPORTED_LANGUAGE_CODES, freeform_location)

    @cached_property
    def location_in_v1_active_language(self):
        v1_active_language = get_language()
        return get_message_in_language(self.cached_location, v1_active_language)

    @transaction.atomic
    def set_dimension_values(self, values_to_set: Mapping[str, Collection[str]], cache: DimensionCache):
        """
        Changes only those dimension values that are present in dimension_values.

        NOTE: Caller must call refresh_cached_dimensions() or refresh_cached_dimensions_qs()
        afterwards to update the cached_dimensions field.

        :param values_to_set: Mapping of dimension slug to list of value slugs.
        :param cache: Cache from Universe.preload_dimensions()
        """
        from .schedule_item_dimension_value import ScheduleItemDimensionValue

        set_dimension_values(ScheduleItemDimensionValue, self, values_to_set, cache)

    def with_mandatory_fields(self) -> Self:
        if not self.slug:
            self.slug = self._make_slug()

        self.cached_event = self.program.event
        self.cached_end_time = self.start_time + self.duration

        return self

    def with_annotations(self) -> Self:
        self.cached_combined_annotations = self.program.annotations.copy()
        self.cached_combined_annotations.update(self.annotations)
        return self

    def with_cached_fields(self) -> Self:
        self.with_mandatory_fields()
        self.with_annotations()
        self.refresh_technical_dimensions()

        self.cached_dimensions = build_cached_dimensions(self.dimensions.all())
        self.cached_combined_dimensions = build_cached_dimensions(self.program.dimensions.all(), self.dimensions.all())
        self.cached_location = self._make_location()

        return self

    update_cached_fields: ClassVar[list[str]] = [
        "cached_combined_annotations",
        "cached_combined_dimensions",
        "cached_dimensions",
        "cached_end_time",
        "cached_event",
        "cached_location",
        "updated_at",
    ]

    def refresh_cached_fields(self) -> None:
        self.with_cached_fields().save(update_fields=self.update_cached_fields)

    @classmethod
    def refresh_cached_fields_qs(cls, qs: models.QuerySet[Self], batch_size=400) -> None:
        bulk_update = [item.with_cached_fields() for item in qs]
        cls.objects.bulk_update(
            bulk_update,
            fields=cls.update_cached_fields,
            batch_size=batch_size,
        )
        logger.info("Refreshed cached fields for %d schedule items", len(bulk_update))

    date_cutoff_time: ClassVar[timedelta] = timedelta(hours=4)  # 04:00 local time

    def get_date_dimension_value(self: ScheduleItem, tz: tzinfo | None = None) -> set[str]:
        """
        Return the date dimension value for the schedule item.

        The `date_cutoff_time` is used to determine at which time of the night the date changes.
        Use this to make the wee hours of the night belong to the previous day.
        """
        tz = tz or self.program.event.timezone
        return {
            (self.start_time.astimezone(tz) - self.date_cutoff_time).date().isoformat(),
            (self.cached_end_time.astimezone(tz) - self.date_cutoff_time).date().isoformat(),
        }

    def refresh_technical_dimensions(self):
        cache = self.program.meta.universe.preload_dimensions(["date"])
        self.set_dimension_values(
            {
                "date": self.get_date_dimension_value(),
            },
            cache=cache,
        )

    def refresh_dependents(self):
        self.program.refresh_cached_fields()
        self.ensure_paikkala()

    def ensure_paikkala(self) -> PaikkalaProgram | None:
        from ..integrations.paikkala_integration import paikkalize_schedule_item

        if not self.cached_combined_dimensions.get("paikkala", []):
            return None

        return paikkalize_schedule_item(self)

    @property
    def is_paikkala_time_visible(self):
        return not self.cached_combined_annotations.get("paikkala:hideStartAndEndTime", False)

    @property
    def is_cancelled(self) -> bool:
        """
        TODO(#726) Cancel single schedule item without cancelling the whole program.
        """
        return bool(set(self.cached_combined_dimensions.get("state", [])).intersection({"cancelled", "rejected"}))
