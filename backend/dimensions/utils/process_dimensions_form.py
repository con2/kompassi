from forms.models.field import Field, FieldType
from forms.utils.process_form_data import process_form_data

from ..models.dimension import Dimension


def process_dimensions_form(
    dimensions: list[Dimension],
    form_data: dict[str, str],
) -> dict[str, list[str]]:
    """
    When values for dimensions are selected using a SchemaForm, this function processes the form data
    and returns the values for each dimension.

    Args:
        dimensions: A list of Dimension objects to process.
        form_data: A dictionary of form data to process.

    Returns:
        A dictionary containing the value slugs for each dimension present in dimensions.
    """
    fields_single = [Field.from_dimension(dimension, FieldType.DIMENSION_SINGLE_SELECT) for dimension in dimensions]
    fields_multi = [Field.from_dimension(dimension, FieldType.DIMENSION_MULTI_SELECT) for dimension in dimensions]

    values_single, warnings_single = process_form_data(fields_single, form_data)
    if warnings_single:
        raise ValueError(warnings_single)

    values_multi, warnings_multi = process_form_data(fields_multi, form_data)
    if warnings_multi:
        raise ValueError(warnings_multi)

    values: dict[str, list[str]] = {k: [v] for k, v in values_single.items() if v}
    for k, v in values_multi.items():
        values.setdefault(k, []).extend(v)

    return values
