from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Self

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db import models
from django.http import QueryDict
from django.utils.timezone import now

from dimensions.filters import DimensionFilters
from dimensions.graphql.dimension_filter_input import DimensionFilterInput
from forms.models.response import Response
from forms.utils.process_form_data import FALSY_VALUES

from .models.program import Program
from .models.schedule import ScheduleItem


def ensure_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt


def parse_datetime(s: str) -> datetime:
    """
    If there is no timezone info, assume UTC.
    """
    return ensure_aware(datetime.fromisoformat(s))


@dataclass
class ProgramFilters:
    slugs: list[str] | None = None
    favorites_only: bool = False
    hide_past: bool = False
    updated_after: datetime | None = None
    dimension_filters: DimensionFilters = field(default_factory=DimensionFilters)

    @classmethod
    def from_query_dict(
        cls,
        filters: QueryDict | dict[str, list[str]],
    ) -> Self:
        if isinstance(filters, QueryDict):
            filters = {k: [str(v) for v in vs] for k, vs in filters.lists()}

        filters = {
            dimension_slug: [slug for slugs in value_slugs for slug in slugs.split(",")]
            for (dimension_slug, value_slugs) in filters.items()
        }

        # filter programs by slug (may be ?slug=a&slug=b or ?slug=a,b,c)
        slugs = filters.pop("slug", [])
        favorites_only = any(v.lower() not in FALSY_VALUES for v in filters.pop("favorited", []))
        hide_past = all(v.lower() in FALSY_VALUES for v in filters.pop("past", []))

        updated_after = (
            parse_datetime(updated_after_str)
            if (updated_after_strs := filters.pop("updated_after", []))
            and (updated_after_str := max(updated_after_strs))
            else None
        )

        return cls(
            slugs=slugs,
            dimension_filters=DimensionFilters(filters=filters),
            favorites_only=favorites_only,
            hide_past=hide_past,
            updated_after=updated_after,
        )

    @classmethod
    def from_graphql(
        cls,
        filters: list[DimensionFilterInput] | None,
        favorites_only: bool = False,
        hide_past: bool = False,
        updated_after: datetime | None = None,
    ):
        return cls(
            dimension_filters=DimensionFilters.from_graphql(filters),  # type: ignore
            favorites_only=favorites_only,
            hide_past=hide_past,
            updated_after=ensure_aware(updated_after) if updated_after else None,
        )

    def filter_program(
        self,
        programs: models.QuerySet[Program],
        user: AbstractBaseUser | AnonymousUser | None = None,
        t: datetime | None = None,
    ):
        if self.slugs:
            programs = programs.filter(slug__in=self.slugs)

        if self.favorites_only:
            if user and user.is_authenticated:
                programs = programs.filter(schedule_items__favorited_by=user)
            else:
                programs = programs.none()

        programs = self.dimension_filters.filter(programs)

        if self.hide_past:
            if t is None:
                t = now()
            programs = programs.filter(cached_latest_end_time__gte=t)

        if self.updated_after:
            programs = programs.filter(updated_at__gt=self.updated_after)

        return (
            programs.distinct()
            .select_related("event")
            .prefetch_related(
                "schedule_items",
                "schedule_items__cached_event",
            )
            .order_by("cached_earliest_start_time")
        )

    def filter_schedule_items(
        self,
        schedule_items: models.QuerySet[ScheduleItem],
        user: AbstractBaseUser | AnonymousUser | None = None,
        t: datetime | None = None,
    ):
        if self.slugs:
            schedule_items = schedule_items.filter(slug__in=self.slugs)

        if self.favorites_only:
            if user and user.is_authenticated:
                schedule_items = schedule_items.filter(favorited_by=user)
            else:
                schedule_items = schedule_items.none()

        # XXX have to implement DimensionFilters.filter ourselves due to indirect access
        # perhaps this will be fixed when dimensions are pushed to ScheduleItem level?
        for dimension_slug, value_slugs in self.dimension_filters.filters.items():
            value_slugs = [slug for slugs in value_slugs for slug in slugs.split(",")]
            if "*" in value_slugs:
                schedule_items = schedule_items.filter(program__dimensions__value__dimension__slug=dimension_slug)
            else:
                schedule_items = schedule_items.filter(
                    program__dimensions__value__dimension__slug=dimension_slug,
                    program__dimensions__value__slug__in=value_slugs,
                )

        if self.hide_past:
            if t is None:
                t = now()
            schedule_items = schedule_items.filter(cached_end_time__gte=t)

        if self.updated_after:
            schedule_items = schedule_items.filter(updated_at__gt=self.updated_after)

        return (
            schedule_items.distinct()
            .select_related(
                "cached_event",
                "program__event",
                "program",
            )
            .order_by("start_time")
        )

    def filter_program_offers(
        self,
        program_offers: models.QuerySet[Response],
    ):
        return self.dimension_filters.filter(program_offers)
