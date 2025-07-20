from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any

from django.db import models

from forms.models.field import Field, FieldType

from .enums import AnnotationDataType

if TYPE_CHECKING:
    from .event_annotation import EventAnnotation

logger = getLogger("kompassi")


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

    def conform_value(self, field: Field, value: Any) -> str | int | float | bool | None:
        if value is None:
            return None

        match self.type, field.type:
            case AnnotationDataType.BOOLEAN, FieldType.SINGLE_CHECKBOX:
                if not isinstance(value, bool):
                    logger.warning(
                        "process_form_data should have returned a boolean: %s",
                        dict(
                            field_slug=field.slug,
                            annotation_type=self.type.value,
                            field_type=field.type.value,
                            value=value,
                        ),
                    )
                    return None
            case AnnotationDataType.BOOLEAN, _:
                # :shrug:
                return bool(value)
            case AnnotationDataType.STRING, _:
                value = str(value)
            case AnnotationDataType.NUMBER, FieldType.NUMBER_FIELD | FieldType.DECIMAL_FIELD:
                if not isinstance(value, (int, float)):
                    logger.warning(
                        "process_form_data should have returned a number: %s",
                        dict(
                            field_slug=field.slug,
                            annotation_type=self.type.value,
                            field_type=field.type.value,
                            value=value,
                        ),
                    )
                    value = None
            case AnnotationDataType.NUMBER, _:
                # :shrug:
                try:
                    value = float(value)
                except ValueError:
                    logger.warning(
                        "value did not float: %s",
                        dict(
                            field_slug=field.slug,
                            annotation_type=self.type.value,
                            field_type=field.type.value,
                            value=value,
                        ),
                    )
                    value = None
            case annotation_type, field_type:
                raise NotImplementedError((annotation_type, field_type))

        return value

    def validate_value(self, value: Any):
        """
        Raises ValueError if the value is not valid for the annotation type.
        """
        if self.type == AnnotationDataType.STRING and not isinstance(value, str):
            raise ValueError(f"Value for {self.type!r} must be a string.")
        if self.type == AnnotationDataType.NUMBER and not isinstance(value, (int, float)):
            raise ValueError(f"Value for {self.type!r} must be a number.")
        if self.type == AnnotationDataType.BOOLEAN and not isinstance(value, bool):
            raise ValueError(f"Value for {self.type!r} must be a boolean.")

    @classmethod
    def ensure(cls):
        from .annotation_dto import ANNOTATIONS, AnnotationDTO

        AnnotationDTO.save_many(ANNOTATIONS)
