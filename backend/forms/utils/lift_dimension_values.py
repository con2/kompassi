from __future__ import annotations

import logging
from collections import defaultdict
from typing import TYPE_CHECKING

from dimensions.utils.dimension_cache import DimensionCache

from ..models.field import Field, FieldType
from ..models.response import Response

if TYPE_CHECKING:
    pass


logger = logging.getLogger("kompassi")


def lift_dimension_values(
    response: Response,
    *,
    dimension_slugs: list[str] | None = None,
    cache: DimensionCache,
):
    """
    Lifts the values of dimensions from form data into proper dimension values.
    This makes sense only for responses that are related to a survey.

    NOTE: Caller must call refresh_cached_fields() or refresh_cached_fields_qs()
    afterwards to update the cached_dimensions field.

    :param dimension_slugs: If provided, only these dimensions will be lifted.
    """
    survey = response.survey

    # only these fields have the potential of being dimension fields
    # TODO support single checkbox as dimension field?
    # get_processed_form_data expects enriched, validated form of fields
    fields: list[Field] = [field for field in response.form.validated_fields if field.type.is_dimension_field]

    if dimension_slugs is not None:
        # filter out fields that are not in dimension_slugs
        fields = [field for field in fields if field.dimension in dimension_slugs]

    values, warnings = response.get_processed_form_data(fields)
    values_to_set: defaultdict[str, set[str]] = defaultdict(set)

    for field in fields:
        log_context = dict(
            scope=survey.scope.slug,
            survey=survey.slug,
            language=response.form.language,
            response=response.id,
            field=field.slug,
            dimension=field.dimension,
            field_type=field.type,
        )

        if not field.dimension:
            logger.warning("Dimension field has no dimension: %s", log_context)
            continue

        dimension = cache.dimensions.get(field.dimension)
        if dimension is None:
            logger.warning(
                "Dimension field refers to non-existing dimension: %s",
                dict(log_context),
            )
            continue

        if field_warnings := warnings.get(field.slug):
            # this dimension has validation warnings
            logger.warning(
                "Cowardly refusing to lift dimension values from field with warnings: %s",
                dict(log_context, warnings=field_warnings, values=values.get(field.slug, [])),
            )
            continue

        value_slugs: list[str]
        match field.type:
            case FieldType.DIMENSION_MULTI_SELECT:
                value_slugs = values.get(field.slug, [])
            case FieldType.DIMENSION_SINGLE_SELECT:
                value_slugs = [value_slug] if (value_slug := values.get(field.slug)) else []
            case FieldType.DIMENSION_SINGLE_CHECKBOX:
                value_slugs = ["true"] if values.get(field.slug) else ["false"]
            case _:
                logger.warning("Unexpected field type for dimension field: %s", log_context)
                continue

        if not isinstance(value_slugs, list):
            logger.warning(
                "Expected list of value slugs for dimension field: %s",
                dict(log_context, value_slugs=value_slugs),
            )
            continue

        for value_slug in value_slugs:
            value = cache.values_by_dimension[dimension.slug][value_slug]
            if value is None:
                logger.warning(
                    "Response refers to a dimension value that doesn't exist: %s",
                    dict(log_context, value_slug=value_slug),
                )
                continue

            values_to_set[dimension.slug].add(value_slug)

    if values_to_set:
        response.set_dimension_values(values_to_set, cache)

    return values_to_set
