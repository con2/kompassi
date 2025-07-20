from collections.abc import Iterable
from typing import Annotated, Any

import pydantic
from pydantic_core import CoreSchema, SchemaValidator, core_schema

from ..models.annotation import Annotation

AnnotationSlug = Annotated[
    str,
    pydantic.StringConstraints(
        min_length=1,
        pattern=r"^[a-zA-Z0-9-_:]+$",
    ),
]

CachedAnnotations = dict[AnnotationSlug, str | int | float | bool]

adapter = pydantic.TypeAdapter(CachedAnnotations)


def build_core_schema(schema: Iterable[Annotation]) -> CoreSchema:
    return core_schema.typed_dict_schema(
        {annotation.slug: core_schema.typed_dict_field(annotation.type.core_schema) for annotation in schema},
        total=False,
    )


def validate_annotations(
    annotations: Any,
    schema: Iterable[Annotation],
) -> CachedAnnotations:
    core_schema = build_core_schema(schema)
    validator = SchemaValidator(core_schema)
    return validator.validate_python(annotations)


def compact_annotations(annotations: CachedAnnotations) -> CachedAnnotations:
    return {k: v for (k, v) in annotations.items() if v not in (None, "")}
