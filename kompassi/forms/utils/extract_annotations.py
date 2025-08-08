import logging
from collections.abc import Iterable

from kompassi.dimensions.models.annotation import Annotation
from kompassi.dimensions.models.cached_annotations import CachedAnnotations
from kompassi.dimensions.models.universe_annotation import UniverseAnnotation

from ..models.response import Response

logger = logging.getLogger(__name__)


def extract_annotations_from_responses(
    responses: Iterable[Response],
    universe_annotations: Iterable[UniverseAnnotation],
) -> CachedAnnotations:
    schema: list[Annotation] = []
    field_mapping: dict[str, list[str]] = {}
    interesting_fields: set[str] = set()

    for ea in universe_annotations:
        schema.append(ea.annotation)
        field_mapping[ea.annotation.slug] = ea.form_fields
        interesting_fields.update(ea.form_fields)

    result: CachedAnnotations = {}

    for response in responses:
        fields = response.form.validated_fields
        values, warnings = response.get_processed_form_data(fields=fields, field_slugs=interesting_fields)
        form_fields_by_slug = {field.slug: field for field in fields}

        for annotation in schema:
            for form_field_slug in field_mapping[annotation.slug]:
                form_field = form_fields_by_slug.get(form_field_slug)
                if form_field is None:
                    # this form does not have this field
                    continue

                value = values.get(form_field_slug)
                if value is None:
                    # no value for this field in this response
                    continue

                if field_warnings := warnings.get(form_field_slug):
                    logger.info(
                        "Cowardly refusing to look for value for annotation in a field with warnings: %s",
                        dict(
                            response=response.id,
                            annotation_slug=annotation.slug,
                            form_field_slug=form_field_slug,
                            field_warnings=field_warnings,
                        ),
                    )
                    continue

                value = annotation.type.conform_value(value)
                if value is None:
                    # value did not conform to the data type of the annotation
                    continue

                result[annotation.slug] = value
                break

    return result
