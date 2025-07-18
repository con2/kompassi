from collections.abc import Iterable
from typing import Annotated, Any

import pydantic

from ..models.annotation import Annotation

AnnotationSlug = Annotated[
    str,
    pydantic.StringConstraints(
        min_length=1,
        pattern=r"^[a-zA-Z0-9-_]+:[a-zA-Z0-9-_]+$",
    ),
]

CachedAnnotations = dict[AnnotationSlug, str | int | float | bool]

adapter = pydantic.TypeAdapter(CachedAnnotations)


def validate_annotations(
    annotations: Any,
    schema: Iterable[Annotation],
) -> CachedAnnotations:
    schema_by_slug = {annotation.slug: annotation for annotation in schema}
    annotations_ = adapter.validate_python(annotations)

    for slug, value in annotations_.items():
        schemoid = schema_by_slug.get(slug)
        if schemoid is None:
            raise ValueError(f"Unknown annotation slug: {slug}")

        schemoid.validate_value(value)

    return annotations_
