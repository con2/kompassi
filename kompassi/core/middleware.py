"""
On-demand per-request cache facility.
Define cached items as cached_properties on PerEventCache or PerRequestCache.
"""

from __future__ import annotations

from enum import Enum
from functools import cached_property
from typing import TYPE_CHECKING

from django.http import HttpRequest

from kompassi.access.cbac import (
    CBACPermissionDenied,
    HasImmutableScope,
    HasScope,
    HasScopeForeignKey,
    Operation,
    make_graphql_claims,
)
from kompassi.core.models.event import Event
from kompassi.dimensions.utils.dimension_cache import DimensionCache

if TYPE_CHECKING:
    from kompassi.dimensions.models.dimension import Dimension
    from kompassi.dimensions.models.dimension_value import DimensionValue
    from kompassi.dimensions.models.universe import Universe
    from kompassi.dimensions.utils.dimension_value_usage import DimensionValueUsage


class EventCache:
    event: Event

    def __init__(self, event: Event):
        self.event = event


class UniverseCache:
    universe: Universe

    def __init__(self, universe: Universe):
        self.universe = universe

    @cached_property
    def dimension_value_usage(self) -> dict[int, dict[int, DimensionValueUsage]]:
        from kompassi.dimensions.utils.dimension_value_usage import DimensionValueUsage

        return DimensionValueUsage.for_universe(universe=self.universe)

    def is_dimension_value_in_use(self, value: DimensionValue) -> bool:
        return value.id in self.dimension_value_usage.get(value.dimension_id, {})

    def is_dimension_in_use(self, dimension: Dimension) -> bool:
        return dimension.id in self.dimension_value_usage

    @cached_property
    def dimension_cache(self) -> DimensionCache:
        return self.universe.preload_dimensions()

    @cached_property
    def annotations(self):
        return self.universe.annotations.all()


class RequestLocalCache:
    request: HttpRequest
    _event_cache: dict[str, EventCache] = {}
    _universe_cache: dict[int, UniverseCache] = {}

    # event id -> UniverseCache
    _program_universe_cache: dict[int, UniverseCache] = {}

    def __init__(self, request: HttpRequest):
        self.request = request

    def for_event(self, event: Event) -> EventCache:
        if event.slug not in self._event_cache:
            self._event_cache[event.slug] = EventCache(event=event)
        return self._event_cache[event.slug]

    def for_universe(self, universe: Universe) -> UniverseCache:
        if universe.id not in self._universe_cache:
            self._universe_cache[universe.id] = UniverseCache(universe=universe)
        return self._universe_cache[universe.id]

    def for_program_universe(self, event: Event) -> UniverseCache:
        """
        To avoid O(n) queries to program.event.program_universe
        """
        if event.id not in self._program_universe_cache:
            universe = event.program_universe
            cache = UniverseCache(universe=universe)
            self._program_universe_cache[event.id] = cache
            self._universe_cache[universe.id] = cache
        return self._program_universe_cache[event.id]

    @cached_property
    def cbac_permissions(self) -> dict[frozenset[tuple[str, str]], bool]:
        from kompassi.access.models.cbac_entry import CBACEntry

        return {
            frozenset((k, v) for k, v in claims.items()): True
            for claims in CBACEntry.get_entries(self.request.user).values_list("claims", flat=True)
        }

    def has_cbac_permission(self, claims: dict[str, str]) -> bool:
        """
        If you are testing multiple permissions during a single request,
        use this method to cache permissions.
        """
        action_pairs = frozenset((k, v) for k, v in claims.items())

        if action_pairs in self.cbac_permissions:
            return True

        for permission_pairs in self.cbac_permissions:
            if permission_pairs.issubset(action_pairs):
                self.cbac_permissions[permission_pairs] = True
                return True

        self.cbac_permissions[action_pairs] = False
        return False

    def mock_permissions(self, *claimses: dict[str, str]) -> None:
        self.cbac_permissions = {}
        for claims in claimses:
            action_pairs = frozenset((k, v) for k, v in claims.items())
            self.cbac_permissions[action_pairs] = True

    def is_allowed(
        self,
        *,
        instance: HasScope | HasImmutableScope | HasScopeForeignKey,
        app: Enum | str,
        operation: Operation = "query",
        field: str = "self",
    ) -> bool:
        claims = make_graphql_claims(
            scope=instance.scope,  # type: ignore
            model=instance.__class__.__name__,
            operation=operation,
            app=app,
            field=field,
        )

        return self.has_cbac_permission(claims)

    def check_permission(
        self,
        *,
        instance: HasScope | HasImmutableScope | HasScopeForeignKey,
        app: Enum | str,
        operation: Operation = "query",
        field: str = "self",
    ):
        claims = make_graphql_claims(
            scope=instance.scope,  # type: ignore
            model=instance.__class__.__name__,
            operation=operation,
            app=app,
            field=field,
        )

        if not self.has_cbac_permission(claims):
            raise CBACPermissionDenied(claims)


class RequestWithCache(HttpRequest):
    """
    Use in annotations only, do not try to instantiate.
    """

    kompassi_cache: RequestLocalCache


def request_cache_middleware(get_response):
    def middleware(request: RequestWithCache):
        request.kompassi_cache = RequestLocalCache(request=request)
        return get_response(request)

    return middleware
