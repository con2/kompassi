from __future__ import annotations

import logging
from collections.abc import Iterable, Mapping
from itertools import batched
from typing import TYPE_CHECKING, Self

import pydantic
from django.contrib.postgres.fields import HStoreField
from django.db import models

from core.utils import validate_slug
from core.utils.locale_utils import get_message_in_language
from graphql_api.language import DEFAULT_LANGUAGE

from .program import Program

if TYPE_CHECKING:
    from core.models import Event


logger = logging.getLogger("kompassi")
DIMENSION_SLUG_MAX_LENGTH = 255


class ValueOrdering(models.TextChoices):
    MANUAL = "manual", "Manual"
    SLUG = "slug", "Alphabetical (slug)"
    TITLE = "title", "Alphabetical (localized title)"


class Dimension(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="program_dimensions")
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

    value_ordering = models.CharField(
        choices=ValueOrdering.choices,
        default=ValueOrdering.TITLE,
        help_text=(
            "In which order are the values of this dimension returned in the GraphQL API. "
            "NOTE: When using Alphabetical (localized title), "
            "the language needs to be provided to `values` and `values.title` fields separately."
        ),
    )

    order = models.SmallIntegerField(default=0)

    values: models.QuerySet[DimensionValue]

    class Meta:
        unique_together = ("event", "slug")
        ordering = ("event", "order")

    def __str__(self):
        return self.slug

    @classmethod
    def dump_dimensions(cls, event: Event):
        for dimension in event.program_dimensions.all():
            print(dimension)
            for value in dimension.values.all():
                print("-", value)

    def get_values(self, lang: str = DEFAULT_LANGUAGE) -> list[DimensionValue]:
        """
        Use this method instead of self.values.all() when you want the values in the correct order.
        NOTE: If value_ordering is TITLE, you need to provide the language.
        """
        values = self.values.all()

        match self.value_ordering:
            case "manual":
                return list(values.order_by("order"))
            case "slug":
                return list(values.order_by("slug"))
            case "title":
                return sorted(values, key=lambda value: get_message_in_language(value.title, lang) or value.slug)
            case _:
                raise NotImplementedError(f"Unknown value_ordering: {self.value_ordering}")


class DimensionValue(models.Model):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="values")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = HStoreField(blank=True, default=dict)
    color = models.CharField(max_length=63, blank=True, default="")

    order = models.SmallIntegerField(
        default=0,
        help_text="Only applies if `dimension.value_ordering` is `manual`.",
    )

    def __str__(self):
        return self.slug

    @property
    def event(self) -> Event:
        return self.dimension.event

    class Meta:
        unique_together = ("dimension", "slug")
        ordering = ("dimension__order", "order")


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

        # NOTE: only implements the `manual` ordering for now
        # See https://con2.slack.com/archives/C3ZGNGY48/p1718446605681339
        ordering = ("dimension__order", "value__order")

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
        dimension_values: Mapping[str, Iterable[str]],
        dimensions_by_slug: dict[str, Dimension],
        values_by_slug: dict[str, dict[str, DimensionValue]],
    ) -> list[Self]:
        bulk_create = []

        for dimension_slug, value_slugs in dimension_values.items():
            dimension = dimensions_by_slug[dimension_slug]
            for value_slug in set(value_slugs):
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
        upsertables: Iterable[Self],
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
    value_ordering: ValueOrdering = pydantic.Field(default=ValueOrdering.TITLE)

    @classmethod
    def save_many(
        cls,
        event: Event,
        dimension_dtos: list[Self],
        remove_others=False,
        refresh_cached=True,
        dimension_value_batch_size=200,
    ) -> list[Dimension]:
        dimensions_upsert = (
            Dimension(
                event=event,
                slug=dimension_dto.slug,
                title=dimension_dto.title,
                is_list_filter=dimension_dto.is_list_filter,
                is_shown_in_detail=dimension_dto.is_shown_in_detail,
                is_negative_selection=dimension_dto.is_negative_selection,
                value_ordering=dimension_dto.value_ordering.value,
                order=order * 10,
            )
            for order, dimension_dto in enumerate(dimension_dtos)
        )
        django_dimensions = Dimension.objects.bulk_create(
            dimensions_upsert,
            update_conflicts=True,
            unique_fields=(
                "event",
                "slug",
            ),
            update_fields=(
                "title",
                "is_list_filter",
                "is_shown_in_detail",
                "is_negative_selection",
                "value_ordering",
                "order",
            ),
        )
        logger.info("Saved %s dimensions", len(django_dimensions))

        values_upsert = (
            DimensionValue(
                dimension=dim_dj,
                slug=choice.slug,
                title=choice.title,
                color=choice.color,
                order=order * 10,
            )
            for (dim_dto, dim_dj) in zip(dimension_dtos, django_dimensions, strict=True)
            for order, choice in enumerate(dim_dto.choices or [])
        )
        num_dvs = 0
        for page, value_batch in enumerate(batched(values_upsert, dimension_value_batch_size)):
            num_dvs += len(
                DimensionValue.objects.bulk_create(
                    value_batch,
                    update_conflicts=True,
                    unique_fields=("dimension", "slug"),
                    update_fields=("title", "color", "order"),
                )
            )
            logger.info("Saved page %s of dimension values", page + 1)
        logger.info("Saved %s dimension values", num_dvs)

        for dim_dto, dim_dj in zip(dimension_dtos, django_dimensions, strict=True):
            values_to_keep = [choice.slug for choice in dim_dto.choices or []]
            _, deleted = dim_dj.values.exclude(slug__in=values_to_keep).delete()
            logger.info("Stale dimension value cleanup for %s deleted %s", dim_dto.slug, deleted or "nothing")

        if remove_others:
            dimensions_to_keep = [dim_dto.slug for dim_dto in dimension_dtos]
            num_deleted_dvs, _ = Dimension.objects.filter(event=event).exclude(slug__in=dimensions_to_keep).delete()
            logger.info("Deleted %s stale dimensions", num_deleted_dvs)

        if refresh_cached:
            Program.refresh_cached_dimensions_qs(event.programs.all())

        return django_dimensions


# shorthand types
CachedDimensions = dict[str, list[str]]
DimensionInput = dict[str, str | list[str] | None]
