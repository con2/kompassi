from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Self

import pydantic
from django.contrib.postgres.fields import HStoreField
from django.db import models

from core.utils import validate_slug

from .program import Program

if TYPE_CHECKING:
    from core.models import Event


logger = logging.getLogger("kompassi")
DIMENSION_SLUG_MAX_LENGTH = 255


class Dimension(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="dimensions")
    slug = models.CharField(max_length=DIMENSION_SLUG_MAX_LENGTH, validators=[validate_slug])
    title = HStoreField(blank=True, default=dict)
    is_multi_value = models.BooleanField(
        default=False,
        help_text=(
            "Suggests to UI that this dimension is likely to have multiple values selected. "
            "NOTE: In the database, all dimensions are multi-value, so this is just a UI hint."
        ),
    )
    is_list_filter = models.BooleanField(
        default=True,
        help_text="Suggests to UI that this dimension should be shown as a list filter.",
    )
    is_shown_in_detail = models.BooleanField(
        default=True,
        help_text="Suggests to UI that this dimension should be shown in detail view.",
    )
    is_negative_selection = models.BooleanField(
        default=False,
        help_text=(
            "Suggests to UI that when this dimension is not being filtered on, all values should be selected. "
            "Intended for use cases when the user is expected to rather exclude certain values than only include some. "
            "One such use case is accessibility and content warnings. "
            "NOTE: Does not make sense without `is_multi_value`."
        ),
    )

    values: models.QuerySet[DimensionValue]

    class Meta:
        unique_together = ("event", "slug")

    def __str__(self):
        return self.slug

    @classmethod
    def dump_dimensions(cls, event: Event):
        for dimension in event.dimensions.all():
            print(dimension)
            for value in dimension.values.all():
                print("-", value)


class DimensionValue(models.Model):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="values")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = HStoreField(blank=True, default=dict)
    color = models.CharField(max_length=63, blank=True, default="")

    def __str__(self):
        return self.slug

    @property
    def event(self) -> Event:
        return self.dimension.event

    class Meta:
        unique_together = ("dimension", "slug")


class ProgramDimensionValue(models.Model):
    id: int

    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="dimensions",
    )
    dimension = models.ForeignKey(
        Dimension,
        on_delete=models.CASCADE,
        related_name="+",
    )
    value = models.ForeignKey(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.dimension}={self.value}"

    @property
    def event(self) -> Event:
        return self.dimension.event

    class Meta:
        unique_together = ("program", "value")

    @classmethod
    def build_upsert_cache(cls, event: Event) -> tuple[dict[str, Dimension], dict[str, dict[str, DimensionValue]]]:
        """
        Builds a cache you can pass to PDV.build_upsertable(program, dimension_values, *cache) to speed up.
        """
        # cache dimension slug -> value slug -> DimensionValue
        values_by_slug: dict[str, dict[str, DimensionValue]] = {}
        for value in DimensionValue.objects.filter(dimension__event=event).select_related("dimension"):
            values_by_slug.setdefault(value.dimension.slug, {})[value.slug] = value

        # cache slug -> Dimension
        dimensions_by_slug: dict[str, Dimension] = {
            dimension_slug: next(iter(values_by_slug.values())).dimension
            for dimension_slug, values_by_slug in values_by_slug.items()
        }

        return dimensions_by_slug, values_by_slug

    @classmethod
    def build_upsertables(
        cls,
        program: Program,
        dimension_values: dict[str, list[str] | str | None],
        dimensions_by_slug: dict[str, Dimension],
        values_by_slug: dict[str, dict[str, DimensionValue]],
    ) -> list[Self]:
        bulk_create = []

        for dimension_slug, value_slugs in dimension_values.items():
            if isinstance(value_slugs, str):
                value_slugs = [value_slugs]

            if not value_slugs:
                continue

            dimension = dimensions_by_slug[dimension_slug]
            for value_slug in value_slugs:
                value = values_by_slug[dimension_slug][value_slug]
                bulk_create.append(
                    cls(
                        program=program,
                        dimension=dimension,
                        value=value,
                    )
                )

        return bulk_create

    @classmethod
    def bulk_upsert(
        cls,
        upsertables: list[Self],
    ):
        """
        For usage example, see ../importers/solmukohta2024.py

        NOTE: It is your responsibility to call Program.refresh_fields_qs(…) after calling this method.
        """
        return cls.objects.bulk_create(
            upsertables,
            update_conflicts=True,
            unique_fields=("program", "value"),
            update_fields=("dimension",),  # shouldn't change, but just to be safe as we don't call handlers
        )


class DimensionValueDTO(pydantic.BaseModel):
    slug: str
    title: dict[str, str]
    color: str = ""


class DimensionDTO(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    slug: str = pydantic.Field(min_length=1)
    title: dict[str, str]
    choices: list[DimensionValueDTO] | None = pydantic.Field(default=None)
    is_list_filter: bool = pydantic.Field(default=True)
    is_shown_in_detail: bool = pydantic.Field(default=True)
    is_negative_selection: bool = pydantic.Field(default=False)

    @classmethod
    def save_many(cls, event: Event, dimension_dtos: list[Self]):
        dimensions_upsert = [
            Dimension(
                event=event,
                slug=dimension_dto.slug,
                title=dimension_dto.title,
                is_list_filter=dimension_dto.is_list_filter,
                is_shown_in_detail=dimension_dto.is_shown_in_detail,
                is_negative_selection=dimension_dto.is_negative_selection,
            )
            for dimension_dto in dimension_dtos
        ]
        django_dimensions = Dimension.objects.bulk_create(
            dimensions_upsert,
            update_conflicts=True,
            unique_fields=("event", "slug"),
            update_fields=("title", "is_list_filter", "is_shown_in_detail", "is_negative_selection"),
        )

        values_upsert = [
            DimensionValue(
                dimension=dim_dj,
                slug=choice.slug,
                title=choice.title,
                color=choice.color,
            )
            for (dim_dto, dim_dj) in zip(dimension_dtos, django_dimensions, strict=True)
            for choice in dim_dto.choices or []
        ]
        DimensionValue.objects.bulk_create(
            values_upsert,
            update_conflicts=True,
            unique_fields=("dimension", "slug"),
            update_fields=("title", "color"),
        )

        for dim_dto, dim_dj in zip(dimension_dtos, django_dimensions, strict=True):
            values_to_keep = [choice.slug for choice in dim_dto.choices or []]
            DimensionValue.objects.filter(dimension=dim_dj).exclude(slug__in=values_to_keep).delete()

        Program.refresh_cached_dimensions_qs(event.programs.all())

        return django_dimensions
