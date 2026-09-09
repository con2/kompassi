from __future__ import annotations

from datetime import UTC, datetime
from typing import Self

import pydantic
from django.db import models

from kompassi.dimensions.graphql.dimension_filter_input import DimensionFilterInput

from .models.entry import Entry

# Sentinel actor filter value standing in for entries with no actor (actor_id is null),
# shown to the user as "System". Must match the frontend's synthesized actor dimension value.
SYSTEM_ACTOR_SLUG = "system"


class EventLogFilters(pydantic.BaseModel):
    month: str | None = None
    entry_type: list[str] = pydantic.Field(default_factory=list)
    actor: list[str] = pydantic.Field(default_factory=list)

    @classmethod
    def from_graphql(cls, filters: list[DimensionFilterInput] | None) -> Self:
        by_slug = {filter.dimension: filter.values for filter in filters} if filters else {}

        month_values = by_slug.get("month")
        entry_type_values = by_slug.get("type")
        actor_values = by_slug.get("actor")

        return cls(
            month=month_values[0] if month_values else None,
            entry_type=entry_type_values or [],
            actor=actor_values or [],
        )

    @property
    def year_month(self) -> tuple[int, int]:
        if self.month:
            year, month = self.month.split("-")
            return int(year), int(month)

        today = datetime.now(UTC).date()
        return today.year, today.month

    def filter(self, queryset: models.QuerySet[Entry]) -> models.QuerySet[Entry]:
        year, month = self.year_month
        queryset = Entry.year_month_filter(queryset, year, month)

        if self.entry_type:
            queryset = queryset.filter(entry_type__in=self.entry_type)

        if self.actor:
            actor_ids = [value for value in self.actor if value != SYSTEM_ACTOR_SLUG]
            actor_filter = models.Q()
            if actor_ids:
                actor_filter |= models.Q(actor_id__in=actor_ids)
            if SYSTEM_ACTOR_SLUG in self.actor:
                actor_filter |= models.Q(actor_id__isnull=True)
            queryset = queryset.filter(actor_filter)

        return queryset
