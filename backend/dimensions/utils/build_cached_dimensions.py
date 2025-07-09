from collections import defaultdict

from django.db import models

from ..models.cached_dimensions import StrictCachedDimensions


def build_cached_dimensions(*querysets: models.QuerySet) -> StrictCachedDimensions:
    """
    Given one or more query sets of model instances following the SubjectDimensionValue
    protocol, this function builds an aggregated dictionary of cached dimensions that
    maps dimension slugs to a list of value slugs.
    """
    dimensions = defaultdict(set)
    for queryset in querysets:
        for item in queryset:
            dimensions[item.value.dimension.slug].add(item.value.slug)

    return {slug: sorted(values) for slug, values in dimensions.items()}
