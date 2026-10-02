import logging
from collections import defaultdict

from ..models.response import Response
from .lift_dimension_values import get_dimension_field_value_slugs

logger = logging.getLogger(__name__)


def extract_dimension_values_from_response(
    response: Response,
    *,
    on_edit: bool = False,
) -> dict[str, list[str]]:
    """
    Returns the dimension values that the fields of the response mark for passing forward.
    Values come from the marked fields only, not from other fields feeding the same dimension.
    Only meaningful when the survey universe is the one the values are passed forward into.
    """
    fields = [
        field
        for field in response.form.validated_fields
        if field.dimension
        and field.type.is_dimension_field
        and (field.propagate_dimension_on_edit if on_edit else field.propagate_dimension_on_create)
    ]
    if not fields:
        return {}

    values, warnings = response.get_processed_form_data(fields)
    result: defaultdict[str, list[str]] = defaultdict(list)

    for field in fields:
        if warnings.get(field.slug):
            continue

        value_slugs = get_dimension_field_value_slugs(
            field,
            values,
            dict(response=response.id, field=field.slug, dimension=field.dimension),
        )
        for value_slug in value_slugs or []:
            if value_slug not in result[str(field.dimension)]:
                result[str(field.dimension)].append(value_slug)

    return dict(result)
