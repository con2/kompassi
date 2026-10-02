from ..models.response import Response


def extract_dimension_values_from_response(
    response: Response,
    *,
    on_edit: bool = False,
) -> dict[str, list[str]]:
    """
    Returns the dimension values of the response that its form fields mark for passing forward.
    Only meaningful when the survey universe is the one the values are passed forward into.
    """
    dimension_slugs = {
        field.dimension
        for field in response.form.validated_fields
        if field.dimension
        and field.type.is_dimension_field
        and (field.propagate_dimension_on_edit if on_edit else field.propagate_dimension_on_create)
    }

    return {
        dimension_slug: list(value_slugs)
        for dimension_slug, value_slugs in response.cached_dimensions.items()
        if dimension_slug in dimension_slugs
    }
