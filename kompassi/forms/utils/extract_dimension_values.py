import logging

from kompassi.dimensions.utils.dimension_cache import DimensionCache

from ..models.response import Response
from .lift_dimension_values import get_dimension_field_value_slugs

logger = logging.getLogger(__name__)


def extract_dimension_values_for_universe(
    response: Response,
    *,
    cache: DimensionCache,
    on_edit: bool = False,
) -> dict[str, list[str]]:
    """
    Returns the values marked for passing forward of the dimension fields that refer to the
    universe of `cache`, whether that is the survey's own universe or the other universe of
    the event. Values are parsed from the form data: those of the other universe are stored
    nowhere else, and reading the own universe the same way keeps each field's value separate.
    """
    survey = response.survey
    fields = [
        field
        for field in response.form.validated_fields
        if field.dimension
        and field.type.is_dimension_field
        and (field.propagate_dimension_on_edit if on_edit else field.propagate_dimension_on_create)
        and survey.resolve_dimension_universe(field.dimension_universe) == cache.universe
    ]
    if not fields:
        return {}

    values, warnings = response.get_processed_form_data(fields)
    result: dict[str, list[str]] = {}

    for field in fields:
        log_context = dict(
            scope=survey.scope.slug,
            survey=survey.slug,
            response=response.id,
            field=field.slug,
            dimension=field.dimension,
            universe=cache.universe.app.value,
        )

        if field_warnings := warnings.get(field.slug):
            logger.warning(
                "Cowardly refusing to pass forward dimension values from field with warnings: %s",
                dict(log_context, warnings=field_warnings),
            )
            continue

        dimension_slug = str(field.dimension)
        known_values = cache.values_by_dimension.get(dimension_slug)
        if known_values is None:
            logger.warning("Dimension field refers to non-existing dimension: %s", log_context)
            continue

        value_slugs = get_dimension_field_value_slugs(field, values, log_context)
        if value_slugs is None:
            continue

        unknown = [value_slug for value_slug in value_slugs if value_slug not in known_values]
        if unknown:
            logger.warning(
                "Response refers to dimension values that do not exist: %s",
                dict(log_context, value_slugs=unknown),
            )

        result[dimension_slug] = [value_slug for value_slug in value_slugs if value_slug in known_values]

    return result
