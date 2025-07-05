from __future__ import annotations

from collections.abc import Collection
from typing import TYPE_CHECKING

from django.db import models

from core.utils.model_utils import make_slug_field

from .enums import DimensionApp
from .scope import Scope

if TYPE_CHECKING:
    from ..utils.dimension_cache import DimensionCache
    from .dimension import Dimension


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

    scope: models.ForeignKey[Scope] = models.ForeignKey(Scope, on_delete=models.CASCADE)
    slug = make_slug_field(unique=False)

    app_name = models.CharField(
        choices=[(app.value, app.name) for app in DimensionApp],
        max_length=max(len(app.value) for app in DimensionApp),
    )

    dimensions: models.QuerySet[Dimension]

    class Meta:
        unique_together = [("scope", "slug")]

    def __str__(self):
        return f"{self.scope}/{self.slug} ({self.app_name})"

    @property
    def app(self) -> DimensionApp:
        return DimensionApp(self.app_name)

    @property
    def surveys(self):
        from forms.models.survey import Survey

        match self.app:
            case DimensionApp.FORMS:
                return Survey.objects.filter(
                    event=self.scope.event,
                    slug=self.slug,
                    app_name=self.app.value,
                )
            case DimensionApp.PROGRAM_V2:
                return Survey.objects.filter(
                    event=self.scope.event,
                    app_name=self.app.value,
                )
            case _:
                raise ValueError(f"Unknown app type: {self.app_name}")

    @property
    def involvements(self):
        from involvement.models.involvement import Involvement

        return Involvement.objects.filter(event=self.scope.event)

    def preload_dimensions(
        self,
        dimension_slugs: Collection[str] | None = None,
        allow_missing: bool = False,
    ) -> DimensionCache:
        from ..utils.dimension_cache import DimensionCache

        return DimensionCache.from_universe(
            self,
            dimension_slugs=dimension_slugs,
            allow_missing=allow_missing,
        )
