from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from django.db.models import QuerySet, TextField, Value
from django.db.models.functions import Concat, Lower

from kompassi.dimensions.filters import DimensionFilters
from kompassi.dimensions.graphql.dimension_filter_input import DimensionFilterInput

if TYPE_CHECKING:
    from .models.involvement import Involvement


@dataclass
class InvolvementFilters:
    dimension_filters: DimensionFilters = field(default_factory=DimensionFilters)
    search: str = ""

    @classmethod
    def from_graphql(
        cls,
        filters: list[DimensionFilterInput] | None = None,
        search: str = "",
    ):
        if filters is None:
            filters = []

        return cls(
            dimension_filters=DimensionFilters.from_graphql(filters),
            search=search,
        )

    def filter(self, queryset: QuerySet[Involvement]) -> QuerySet[Involvement]:
        queryset = self.dimension_filters.filter(queryset)

        if self.search:
            queryset = queryset.annotate(
                search=Lower(
                    Concat(
                        "person__first_name",
                        Value(" "),
                        "person__surname",
                        Value(" "),
                        "person__nick",
                        Value(" "),
                        "person__email",
                        output_field=TextField(),
                    )
                ),
            ).filter(search__contains=self.search.lower())

        return queryset.distinct()
