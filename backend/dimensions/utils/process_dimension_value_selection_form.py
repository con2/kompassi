from collections.abc import Iterable

from forms.models.field import Field, FieldType
from forms.utils.process_form_data import process_form_data

from ..models.cached_dimensions import StrictCachedDimensions, validate_cached_dimensions
from ..models.dimension import Dimension


def process_dimension_value_selection_form(
    dimensions: Iterable[Dimension],
    form_data: dict[str, str],
    *,
    slug_prefix: str = "",
) -> StrictCachedDimensions:
    """
    When values for dimensions are selected using a SchemaForm, this function processes the form data
    and returns the values for each dimension.

    Args:
        dimensions: A list of Dimension objects to process.
        form_data: A dictionary of form data to process.

    Returns:
        A dictionary containing the value slugs for each dimension present in dimensions.
    """
    fields_single = [
        Field.from_dimension(
            dimension,
            FieldType.DIMENSION_SINGLE_SELECT,
            slug_prefix=slug_prefix,
        )
        for dimension in dimensions
    ]
    fields_multi = [
        Field.from_dimension(
            dimension,
            FieldType.DIMENSION_MULTI_SELECT,
            slug_prefix=slug_prefix,
        )
        for dimension in dimensions
    ]

    values_single, warnings_single = process_form_data(fields_single, form_data, slug_prefix=slug_prefix)
    if warnings_single:
        raise ValueError(warnings_single)

    values_multi, warnings_multi = process_form_data(fields_multi, form_data, slug_prefix=slug_prefix)
    if warnings_multi:
        raise ValueError(warnings_multi)

    values: dict[str, set[str]] = {}
    for k, v in values_single.items():
        if v:
            values.setdefault(k, set()).add(v)
    for k, v in values_multi.items():
        values.setdefault(k, set()).update(v)

    # de-setify
    return validate_cached_dimensions(values)
