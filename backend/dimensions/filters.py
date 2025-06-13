from typing import Self, TypeVar

import pydantic
from django.db import models
from django.http import QueryDict

from dimensions.graphql.dimension_filter_input import DimensionFilterInput

T = TypeVar("T", bound=models.Model)


class DimensionFilters(pydantic.BaseModel):
    filters: dict[str, list[str]] = pydantic.Field(default_factory=dict)
    field_name: str = "cached_dimensions"

    @classmethod
    def from_query_dict(
        cls,
        filters: QueryDict | dict[str, list[str]],
        field_name: str = "cached_dimensions",
    ) -> Self:
        if isinstance(filters, QueryDict):
            filters = {k: [str(v) for v in vs] for k, vs in filters.lists()}

        filters = {
            dimension_slug: [slug for slugs in value_slugs for slug in slugs.split(",")]
            for (dimension_slug, value_slugs) in filters.items()
        }

        return cls(
            filters=filters,
            field_name=field_name,
        )

    @classmethod
    def from_graphql(
        cls,
        filters: list[DimensionFilterInput] | None,
        field_name: str = "cached_dimensions",
    ):
        dimensions = (
            {filter.dimension: ["*"] if filter.values is None else filter.values for filter in filters}
            if filters
            else {}
        )

        return cls(
            filters=dimensions,  # type: ignore
            field_name=field_name,
        )

    def filter(
        self,
        queryset: models.QuerySet[T],
    ):
        # optimization: we can check dimensions with only single value or wildcard
        # with a single @> operator query on the GIN index
        fast_dimension_filters = {}

        for dimension_slug, value_slugs in self.filters.items():
            if "*" in value_slugs:
                fast_dimension_filters[dimension_slug] = []
            elif len(value_slugs) == 1:
                fast_dimension_filters[dimension_slug] = value_slugs
            else:
                # slow path: multiple values for the same dimension (OR/ANY semantics within dimension)
                q = models.Q()
                for value_slug in value_slugs:
                    q |= models.Q(**{f"{self.field_name}__contains": {dimension_slug: [value_slug]}})
                queryset = queryset.filter(q)

        if fast_dimension_filters:
            queryset = queryset.filter(**{f"{self.field_name}__contains": fast_dimension_filters})

        return queryset
