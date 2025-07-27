from typing import Protocol

import graphene
from graphene.types.generic import GenericScalar

from kompassi.core.middleware import RequestWithCache
from kompassi.core.models.event import Event
from kompassi.core.utils.text_utils import normalize_whitespace
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.dimensions.models.scope import Scope
from kompassi.dimensions.models.universe import Universe


class _Parent(Protocol):
    event: Event
    cached_dimensions: CachedDimensions
    cached_combined_dimensions: CachedDimensions
    universe: Universe
    scope: Scope


def resolve_cached_dimensions(
    parent: _Parent,
    info,
    # TODO(#806) Change public_only default to True and require authentication
    public_only: bool = False,
    own_only: bool = False,
    key_dimensions_only: bool = False,
    list_filters_only: bool = False,
) -> CachedDimensions:
    """
    Returns a mapping of dimension slugs to lists of value slugs.

    Using `cachedDimensions` is faster than `dimensions` as it requires less joins and database queries.
    The difference is negligible for a single program or schedule item, but when using the plural
    resolvers like `programs` or `scheduleItems`, the performance difference can be significant.

    By default, returns both dimensions set on the program itself and those set on its schedule items.
    If `own_only` is True, only returns dimensions set on this item itself.

    By default, returns both public and internal dimensions. This will change in near future to only
    return public dimensions by default and require `publicOnly: false` to get internal dimensions.
    At that time, the default will change to `publicOnly: true`,
    and setting `publicOnly: false` will require authentication.

    To limit the returned dimensions to key dimensions, set `keyDimensionsOnly: true` (default is `false`).
    To limit the returned dimensions to list filters, set `listFiltersOnly: true` (default is `false`).
    """

    request: RequestWithCache = info.context
    cache = request.kompassi_cache
    dimension_cache = cache.for_program_universe(parent.event).dimension_cache

    if own_only:
        cached_dimensions = parent.cached_dimensions
    else:
        cached_dimensions = parent.cached_combined_dimensions

    if public_only:
        cached_dimensions = {k: v for (k, v) in cached_dimensions.items() if dimension_cache.dimensions[k].is_public}
    else:
        pass
        # TODO(#806) Change public_only default to True and require authentication
        # cache.check_permission(
        #     instance=parent,
        #     app=parent.universe.app_name,
        # )

    if key_dimensions_only:
        cached_dimensions = {
            k: v for (k, v) in cached_dimensions.items() if dimension_cache.dimensions[k].is_key_dimension
        }

    if list_filters_only:
        cached_dimensions = {
            k: v for (k, v) in cached_dimensions.items() if dimension_cache.dimensions[k].is_list_filter
        }

    return cached_dimensions


cached_dimensions = graphene.Field(
    GenericScalar,
    # TODO(#806) Change public_only default to True and require authentication
    public_only=graphene.Boolean(default_value=False),
    own_only=graphene.Boolean(default_value=False),
    key_dimensions_only=graphene.Boolean(default_value=False),
    list_filters_only=graphene.Boolean(default_value=False),
    description=normalize_whitespace(resolve_cached_dimensions.__doc__ or ""),
)
