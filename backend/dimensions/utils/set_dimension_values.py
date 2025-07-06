from django.db import models

from ..models.cached_dimensions import CachedDimensions, validate_cached_dimensions
from .dimension_cache import DimensionCache


def set_dimension_values(
    SubjectDimensionValue: type[models.Model],
    subject: models.Model,
    values_to_set: CachedDimensions,
    cache: DimensionCache,
    batch_size: int = 1000,
):
    """
    Given a subject and its subject dimension value model, sets the value of
    the dimensions present in values_to_set. Values of other dimensions are
    left untouched.

    NOTE: If subject has cached_dimensions (as most consumers of Dimensions do),
    caller must call refresh_cached_dimensions() or refresh_cached_dimensions_qs()
    afterwards to update the cached_dimensions field.

    :param values_to_set: Mapping of dimension slug to list of value slugs.
    :param cache: Cache from Universe.preload_dimensions()
    """
    values_to_set = validate_cached_dimensions(values_to_set)

    SubjectDimensionValue.objects.filter(
        subject=subject,
        value__dimension__slug__in=values_to_set.keys(),
    ).delete()

    SubjectDimensionValue.objects.bulk_create(
        (
            SubjectDimensionValue(
                subject=subject,
                value=cache.values_by_dimension[dimension_slug][value_slug],
            )
            for dimension_slug, value_slugs in values_to_set.items()
            for value_slug in value_slugs
        ),
        unique_fields=("subject", "value"),
        ignore_conflicts=True,
        batch_size=batch_size,
    )
