import logging
from collections.abc import Iterable

from kompassi.dimensions.models.cached_annotations import CachedAnnotations
from kompassi.dimensions.models.universe_annotation import UniverseAnnotation

from ..models.response import Response

logger = logging.getLogger(__name__)


def extract_annotations_from_responses(
    responses: Iterable[Response],
    universe_annotations: Iterable[UniverseAnnotation],
    *,
    on_edit: bool = False,
) -> CachedAnnotations:
    """
    Collects annotation values from fields that declare `propagate_to_annotation`.
    Annotations not active in the given universe annotations are ignored.
    When several fields target the same annotation, the first field with a usable value wins.
    """
    schema = {ua.annotation.slug: ua.annotation for ua in universe_annotations if ua.is_active}

    result: CachedAnnotations = {}

    for response in responses:
        fields = response.form.validated_fields
        propagating_fields = [
            field
            for field in fields
            if field.propagate_to_annotation in schema and (not on_edit or field.propagate_to_annotation_on_edit)
        ]
        if not propagating_fields:
            continue

        values, warnings = response.get_processed_form_data(
            fields=fields,
            field_slugs={field.slug for field in propagating_fields},
        )

        response_result: CachedAnnotations = {}
        for field in propagating_fields:
            annotation = schema[str(field.propagate_to_annotation)]

            if annotation.slug in response_result:
                continue

            value = values.get(field.slug)
            if value is None:
                continue

            if field_warnings := warnings.get(field.slug):
                logger.info(
                    "Cowardly refusing to look for value for annotation in a field with warnings: %s",
                    dict(
                        response=response.id,
                        annotation_slug=annotation.slug,
                        form_field_slug=field.slug,
                        field_warnings=field_warnings,
                    ),
                )
                continue

            value = annotation.type.conform_value(value)
            if value is None:
                continue

            response_result[annotation.slug] = value

        result.update(response_result)

    return result
