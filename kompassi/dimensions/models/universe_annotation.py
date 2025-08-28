from __future__ import annotations

from collections.abc import Iterable

from django.db import models

from .annotation import Annotation
from .universe import Universe


class UniverseAnnotation(models.Model):
    """
    Selects an Annotation to be used in a Universe and
    provides Universe-specific configuration.
    """

    universe = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="all_universe_annotations",
    )
    annotation = models.ForeignKey(
        Annotation,
        on_delete=models.CASCADE,
        related_name="all_universe_annotations",
    )

    is_active = models.BooleanField(default=True)
    form_fields = models.JSONField(
        default=list,
        help_text="Slugs of form fields to extract values from.",
    )

    class Meta:
        unique_together = ("universe", "annotation")

    def __str__(self):
        return f"{self.universe} - {self.annotation}"

    @classmethod
    def ensure(cls, universe: Universe, annotations: Iterable[Annotation] | None = None):
        if annotations is None:
            annotations = Annotation.objects.all()

        # not returning the result because caveats with ignore_conflicts (see doc)
        cls.objects.bulk_create(
            [cls(universe=universe, annotation=annotation) for annotation in annotations],
            ignore_conflicts=True,
        )
