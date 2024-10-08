from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db import models
from django.http import QueryDict
from django.utils.timezone import now

from core.graphql.common import DimensionFilterInput
from forms.utils.process_form_data import FALSY_VALUES

from .models.program import Program
from .models.schedule import ScheduleItem


@dataclass
class ProgramFilters:
    slugs: list[str] | None = None
    dimensions: dict[str, list[str]] = field(default_factory=dict)
    favorites_only: bool = False
    hide_past: bool = False

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

        return cls(
            slugs=slugs,
            dimensions=dict(filters),
            favorites_only=favorites_only,
            hide_past=hide_past,
        )

    @classmethod
    def from_graphql(
        cls,
        filters: list[DimensionFilterInput] | None,
        favorites_only: bool = False,
        hide_past: bool = False,
    ):
        dimensions = {filter.dimension: filter.values for filter in filters} if filters else {}

        return cls(
            dimensions=dimensions,  # type: ignore
            favorites_only=favorites_only,
            hide_past=hide_past,
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
                programs = programs.filter(favorited_by=user)
            else:
                programs = programs.none()

        for dimension_slug, value_slugs in self.dimensions.items():
            value_slugs = [slug for slugs in value_slugs for slug in slugs.split(",")]
            programs = programs.filter(
                dimensions__dimension__slug=dimension_slug,
                dimensions__value__slug__in=value_slugs,
            )

        if self.hide_past:
            if t is None:
                t = now()
            programs = programs.filter(cached_latest_end_time__gte=t)

        return programs.distinct().order_by("cached_earliest_start_time")

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
                schedule_items = schedule_items.filter(program__favorited_by=user)
            else:
                schedule_items = schedule_items.none()

        for dimension_slug, value_slugs in self.dimensions.items():
            value_slugs = [slug for slugs in value_slugs for slug in slugs.split(",")]
            schedule_items = schedule_items.filter(
                program__dimensions__dimension__slug=dimension_slug,
                program__dimensions__value__slug__in=value_slugs,
            )

        if self.hide_past:
            if t is None:
                t = now()
            schedule_items = schedule_items.filter(cached_end_time__gte=t)

        return schedule_items.distinct().order_by("start_time")
