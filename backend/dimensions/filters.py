from typing import Self, TypeVar

import pydantic
from django.db import models
from django.http import QueryDict

from dimensions.graphql.dimension_filter_input import DimensionFilterInput

T = TypeVar("T", bound=models.Model)


class DimensionFilters(pydantic.BaseModel):
    filters: dict[str, list[str]] = pydantic.Field(default_factory=dict)

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

        return cls(
            filters=filters,
        )

    @classmethod
    def from_graphql(
        cls,
        filters: list[DimensionFilterInput] | None,
    ):
        dimensions = (
            {filter.dimension: ["*"] if filter.values is None else filter.values for filter in filters}
            if filters
            else {}
        )

        return cls(
            filters=dimensions,  # type: ignore
        )

    def filter(
        self,
        queryset: models.QuerySet[T],
    ):
        for dimension_slug, value_slugs in self.filters.items():
            value_slugs = [slug for slugs in value_slugs for slug in slugs.split(",")]
            if "*" in value_slugs:
                queryset = queryset.filter(dimensions__value__dimension__slug=dimension_slug)
            else:
                queryset = queryset.filter(
                    dimensions__value__dimension__slug=dimension_slug,
                    dimensions__value__slug__in=value_slugs,
                )

        return queryset.distinct()
