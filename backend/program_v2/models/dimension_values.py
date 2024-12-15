from __future__ import annotations

import logging
from collections.abc import Iterable, Mapping
from typing import Any, Self

from django.db import models

from core.models import Event
from dimensions.models.dimension_value import DimensionValue

from .program import Program
from .schedule import ScheduleItem

logger = logging.getLogger("kompassi")


class DimensionValueMixin:
    objects: Any
    value: Any  # fk to DimensionValue

    def __init__(self, *args, **kwargs): ...

    @classmethod
    def build_upsert_cache(cls, event: Event) -> dict[str, dict[str, DimensionValue]]:
        """
        Builds a cache you can pass to PDV.build_upsertable(program, dimension_values, *cache) to speed up.
        """
        # cache dimension slug -> value slug -> DimensionValue
        values_by_slug: dict[str, dict[str, DimensionValue]] = {}
        for value in DimensionValue.objects.filter(
            dimension__universe=event.program_universe,
        ).select_related("dimension"):
            values_by_slug.setdefault(value.dimension.slug, {})[value.slug] = value

        return values_by_slug

    @classmethod
    def build_upsertables(
        cls,
        program: Program,
        dimension_values: Mapping[str, Iterable[str]],
        values_by_slug: dict[str, dict[str, DimensionValue]],
    ) -> list[Self]:
        bulk_create = []

        for dimension_slug, value_slugs in dimension_values.items():
            for value_slug in set(value_slugs):
                value = values_by_slug[dimension_slug].get(value_slug)
                if value is None:
                    logger.warning("DimensionValue not found: dimension=%s, value=%s", dimension_slug, value_slug)
                    continue

                bulk_create.append(
                    cls(
                        program=program,
                        value=value,
                    )
                )

        return bulk_create

    @classmethod
    def bulk_upsert(
        cls,
        upsertables: Iterable[Self],
        batch_size=400,
    ):
        """
        For usage example, see ../importers/solmukohta2024.py

        NOTE: It is your responsibility to call Program.refresh_fields_qs(…) after calling this method.
        """
        return cls.objects.bulk_create(
            upsertables,
            update_conflicts=True,
            unique_fields=("program", "value"),
            update_fields=("value",),  # HACK but we don't get the ids if ignore_conflicts=True
            batch_size=batch_size,
        )


class ProgramDimensionValue(DimensionValueMixin, models.Model):
    id: int

    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="dimensions",
    )
    value = models.ForeignKey(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.value.dimension}={self.value}"

    class Meta:
        unique_together = ("program", "value")
        ordering = ("value__dimension__order", "value__order")


class ScheduleItemDimensionValue(DimensionValueMixin, models.Model):
    id: int

    schedule_item = models.ForeignKey(
        ScheduleItem,
        on_delete=models.CASCADE,
        related_name="dimensions",
    )
    value = models.ForeignKey(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="+",
    )

    class Meta:
        unique_together = ("schedule_item", "value")
        ordering = ("value__dimension__order", "value__order")
