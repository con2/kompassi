from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass

from ..models.dimension import Dimension
from ..models.dimension_value import DimensionValue
from ..models.universe import Universe


@dataclass
class DimensionCache:
    """
    To avoid O(n) queries for each dimension and dimension value, many operations
    preload all or selected dimensions and their values.

    :param dimension_slugs: Slugs of dimensions to preload.
    :param dimension_values: Slugs of dimension values per dimension to preload.
        Useful when the cache is being used to eg. form a cached_dimensions.
    """

    universe: Universe
    dimensions: dict[str, Dimension]
    values_by_dimension: dict[str, dict[str, DimensionValue]]

    @classmethod
    def from_universe(
        cls,
        universe: Universe,
        dimension_slugs: Collection[str] | None = None,
    ) -> DimensionCache:
        dimensions = universe.dimensions.all().prefetch_related("values")
        if dimension_slugs is not None:
            dimensions = dimensions.filter(slug__in=dimension_slugs)

        dimensions = {dimension.slug: dimension for dimension in dimensions}

        values_by_dimension: dict[str, dict[str, DimensionValue]] = {}
        for dimension in dimensions.values():
            values_by_dimension[dimension.slug] = {value.slug: value for value in dimension.values.all()}

        return cls(
            universe=universe,
            dimensions=dimensions,
            values_by_dimension=values_by_dimension,
        )
