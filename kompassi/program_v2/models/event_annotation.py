from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .annotation import Annotation

if TYPE_CHECKING:
    from .meta import ProgramV2EventMeta

logger = logging.getLogger(__name__)


class EventAnnotation(models.Model):
    pk = models.CompositePrimaryKey("meta", "annotation")

    meta: models.ForeignKey[ProgramV2EventMeta] = models.ForeignKey(
        "program_v2.ProgramV2EventMeta",
        on_delete=models.CASCADE,
        related_name="all_event_annotations",
    )

    annotation: models.ForeignKey[Annotation] = models.ForeignKey(
        "program_v2.Annotation",
        on_delete=models.CASCADE,
        related_name="all_event_annotations",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="If false, this annotation will not be used in this event.",
    )

    program_form_fields = ArrayField(
        models.TextField(),
        default=list,
        blank=True,
        help_text="List of program form field slugs this annotation will be attempted to be extracted from, in order.",
    )

    def __str__(self):
        return f"{self.annotation.slug} ({self.meta.event.slug})"

    @classmethod
    def ensure(cls, meta: ProgramV2EventMeta):
        # TODO only select basic annotations that should be enabled for all events
        annotations = Annotation.objects.all()

        # not returning the result because caveats with ignore_conflicts (see doc)
        cls.objects.bulk_create(
            [cls(meta=meta, annotation=annotation) for annotation in annotations],
            ignore_conflicts=True,
        )
