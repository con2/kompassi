from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .enums import AnnotationDataType

if TYPE_CHECKING:
    from .meta import ProgramV2EventMeta


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

    @property
    def type(self) -> AnnotationDataType:
        return AnnotationDataType(self.type_slug)

    @property
    def is_internal(self) -> bool:
        return self.slug.startswith("internal:")

    def __str__(self):
        return self.slug

    def validate_value(self, value: Any):
        """
        Raises ValueError if the value is not valid for the annotation type.
        """
        if self.type == AnnotationDataType.STRING and not isinstance(value, str):
            raise ValueError(f"Value for {self.slug} must be a string.")
        if self.type == AnnotationDataType.NUMBER and not isinstance(value, (int, float)):
            raise ValueError(f"Value for {self.slug} must be a number.")
        if self.type == AnnotationDataType.BOOLEAN and not isinstance(value, bool):
            raise ValueError(f"Value for {self.slug} must be a boolean.")


class EventAnnotation(models.Model):
    meta: models.ForeignKey[ProgramV2EventMeta] = models.ForeignKey(
        "program_v2.ProgramV2EventMeta",
        on_delete=models.CASCADE,
        related_name="event_annotations",
    )

    annotation: models.ForeignKey[Annotation] = models.ForeignKey(
        "program_v2.Annotation",
        on_delete=models.CASCADE,
        related_name="event_annotations",
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
