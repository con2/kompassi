from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from django.db import models

from .enums import AnnotationDataType

if TYPE_CHECKING:
    from .event_annotation import EventAnnotation

logger = getLogger(__name__)


class Annotation(models.Model):
    slug = models.SlugField(unique=True)
    title = models.JSONField(default=dict)
    description = models.JSONField(default=dict)
    type_slug = models.CharField(
        max_length=50,
        choices=[(typ.value, typ.value) for typ in AnnotationDataType],
        default=AnnotationDataType.STRING.value,
    )

    is_applicable_to_program_items = models.BooleanField(default=True)
    is_applicable_to_schedule_items = models.BooleanField(default=False)

    is_public = models.BooleanField(default=True)
    is_shown_in_detail = models.BooleanField(default=True)
    is_computed = models.BooleanField(default=False)

    all_event_annotations: models.QuerySet[EventAnnotation]

    @property
    def type(self) -> AnnotationDataType:
        return AnnotationDataType(self.type_slug)

    @property
    def is_internal(self) -> bool:
        return self.slug.startswith("internal:")

    def __str__(self):
        return self.slug

    @classmethod
    def ensure(cls):
        from .annotation_dto import ANNOTATIONS, AnnotationDTO

        AnnotationDTO.save_many(ANNOTATIONS)
