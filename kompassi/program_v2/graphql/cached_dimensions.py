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
