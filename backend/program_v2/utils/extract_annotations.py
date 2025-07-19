import logging
from collections.abc import Iterable
from typing import Any

from forms.models.response import Response
from forms.utils.process_form_data import FieldWarning
from program_v2.models.annotation import Annotation
from program_v2.models.event_annotation import EventAnnotation

from ..models.cached_annotations import CachedAnnotations, validate_annotations

logger = logging.getLogger("kompassi")


def extract_annotations(
    values: dict[str, Any],
    warnings: dict[str, list[FieldWarning]],
    schema: list[Annotation],
    field_mapping: dict[str, list[str]],
) -> CachedAnnotations:
    result = {}

    for annotation in schema:
        for form_field_slug in field_mapping.get(annotation.slug, []):
            if field_warnings := warnings.get(form_field_slug):
                logger.info(
                    "Cowardly refusing to look for value for annotation in a field with warnings: %s",
                    dict(
                        annotation_slug=annotation.slug,
                        form_field_slug=form_field_slug,
                        field_warnings=field_warnings,
                    ),
                )
                continue

            if (value := values.get(form_field_slug)) is None:
                continue

            try:
                annotation.validate_value(value)
            except ValueError as e:
                logger.warning(
                    "Invalid value for annotation: %s",
                    dict(
                        annotation_slug=annotation.slug,
                        form_field_slug=form_field_slug,
                        error_message=str(e),
                    ),
                )
                continue

            result[annotation.slug] = value

    return validate_annotations(result, schema)


def extract_annotations_from_responses(
    responses: Iterable[Response],
    event_annotations: Iterable[EventAnnotation],
) -> CachedAnnotations:
    schema: list[Annotation] = []
    field_mapping: dict[str, list[str]] = {}
    interesting_fields: set[str] = set()

    for ea in event_annotations:
        schema.append(ea.annotation)
        field_mapping[ea.annotation.slug] = ea.program_form_fields
        interesting_fields.update(ea.program_form_fields)

    result: CachedAnnotations = {}

    for response in responses:
        values, warnings = response.get_processed_form_data(field_slugs=interesting_fields)
        result.update(
            extract_annotations(
                values=values,
                warnings=warnings,
                schema=schema,
                field_mapping=field_mapping,
            )
        )

    return result
