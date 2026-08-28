from __future__ import annotations

from collections.abc import Collection
from typing import TYPE_CHECKING

from django.db import models
from django_enum import EnumField

from kompassi.core.middleware import RequestWithCache
from kompassi.core.utils.model_utils import make_slug_field

from .enums import DimensionApp
from .scope import Scope

if TYPE_CHECKING:
    from kompassi.involvement.models.involvement import Involvement

    from ..utils.dimension_cache import DimensionCache
    from .annotation import Annotation
    from .dimension import Dimension
    from .universe_annotation import UniverseAnnotation


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

    scope: models.ForeignKey[Scope] = models.ForeignKey(
        Scope,
        on_delete=models.CASCADE,
        related_name="universes",
    )
    slug = make_slug_field(unique=False)

    app: DimensionApp = EnumField(DimensionApp)  # type: ignore

    all_involvements: models.QuerySet[Involvement]
    all_universe_annotations: models.QuerySet[UniverseAnnotation]
    dimensions: models.QuerySet[Dimension]

    id: int
    pk: int

    class Meta:
        unique_together = [("scope", "slug")]  # noqa: RUF012

    def __str__(self):
        return f"{self.scope}/{self.slug} ({self.app})"

    @property
    def active_involvements(self) -> models.QuerySet[Involvement]:
        return self.all_involvements.filter(is_active=True)

    @property
    def active_universe_annotations(self) -> models.QuerySet[UniverseAnnotation]:
        return self.all_universe_annotations.filter(is_active=True)

    @property
    def annotations(self) -> models.QuerySet[Annotation]:
        from .annotation import Annotation

        annotation_ids = self.active_universe_annotations.values_list("annotation_id", flat=True)
        return Annotation.objects.filter(id__in=annotation_ids)

    @property
    def surveys(self):
        from kompassi.forms.models.survey import Survey

        match self.app:
            case DimensionApp.FORMS:
                return Survey.objects.filter(
                    event=self.scope.event,
                    slug=self.slug,
                    app=self.app,
                )
            case DimensionApp.PROGRAM:
                return Survey.objects.filter(
                    event=self.scope.event,
                    app=self.app,
                )
            case _:
                raise ValueError(f"Unknown app type: {self.app}")

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

    def can_dimensions_be_created_by(self, request: RequestWithCache) -> bool:
        return request.kompassi_cache.is_allowed(
            instance=self,
            operation="create",
            field="dimensions",
            app=self.app,
        )
