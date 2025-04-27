from __future__ import annotations

from collections.abc import Collection
from typing import TYPE_CHECKING

from django.db import models

from core.utils.model_utils import make_slug_field

from .scope import Scope

if TYPE_CHECKING:
    from .dimension import Dimension
    from .dimension_value import DimensionValue

APP_CHOICES = [
    ("forms", "Surveys V2"),
    ("program_v2", "Program V2"),
]


class Universe(models.Model):
    """
    A Universe defines a set of Dimensions (with DimensionValues for each).
    A Universe can be attached to many things such as Program items or Surveys.
    There may be one or more Universes for each Scope.
    For example, for Program, there is only one Universe per Scope, and the Atoms
    (things that Dimensions are attached to) are Program items.
    Contrast this to Surveys where generally there is one Universe per Survey –
    hence, multiple Universes per Scope.
    """

    scope = models.ForeignKey(Scope, on_delete=models.CASCADE)
    slug = make_slug_field(unique=False)

    app = models.CharField(
        choices=APP_CHOICES,
        max_length=max(len(choice[0]) for choice in APP_CHOICES),
    )

    dimensions: models.QuerySet[Dimension]

    class Meta:
        unique_together = [("scope", "slug")]

    def __str__(self):
        return f"{self.scope}/{self.slug} ({self.app})"

    @property
    def survey(self):
        if self.app != "forms":
            return None

        from forms.models.survey import Survey

        return Survey.objects.filter(
            event=self.scope.event,
            slug=self.slug,
        ).first()

    def preload_dimensions(
        self,
        dimension_slugs: Collection[str] | None = None,
    ) -> tuple[dict[str, Dimension], dict[str, dict[str, DimensionValue]]]:
        """
        To avoid O(n) queries for each dimension and dimension value, many operations
        preload all or selected dimensions and their values.

        :param dimension_slugs: Slugs of dimensions to preload.
        :param dimension_values: Slugs of dimension values per dimension to preload.
            Useful when the cache is being used to eg. form a cached_dimensions.
        """
        dimensions = self.dimensions.all().prefetch_related("values")
        if dimension_slugs is not None:
            dimensions = dimensions.filter(slug__in=dimension_slugs)

        dimensions_by_slug = {dimension.slug: dimension for dimension in dimensions}

        values_by_dimension_by_slug: dict[str, dict[str, DimensionValue]] = {}
        for dimension in dimensions_by_slug.values():
            values_by_dimension_by_slug[dimension.slug] = {value.slug: value for value in dimension.values.all()}

        return dimensions_by_slug, values_by_dimension_by_slug
