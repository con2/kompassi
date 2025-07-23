from collections.abc import Iterable
from typing import Annotated, Any

import pydantic
from pydantic_core import SchemaValidator, core_schema

from ..models.annotation import Annotation

AnnotationSlug = Annotated[
    str,
    pydantic.StringConstraints(
        min_length=1,
        pattern=r"^[a-zA-Z0-9-_:]+$",
    ),
]

CachedAnnotations = dict[AnnotationSlug, str | int | float | bool]
cached_annotations_adapter = pydantic.TypeAdapter(CachedAnnotations)

# values "" and None used to indicate "remove this annotation"
CachedAnnotationsUpdate = dict[AnnotationSlug, str | int | float | bool | None]
cached_annotations_update_adapter = pydantic.TypeAdapter(CachedAnnotationsUpdate)


def validate_annotations(
    annotations: Any,
    schema: Iterable[Annotation],
) -> CachedAnnotations:
    """
    Perform full schema validation on annotations.
    """
    validator = SchemaValidator(
        core_schema.typed_dict_schema(
            {annotation.slug: core_schema.typed_dict_field(annotation.type.core_schema) for annotation in schema},
            total=False,
        )
    )
    return validator.validate_python(annotations)


def compact_annotations(annotations: CachedAnnotationsUpdate) -> CachedAnnotations:
    """
    Remove empty values from annotations to save space.
    """
    return {k: v for (k, v) in annotations.items() if v not in (None, "")}
