from __future__ import annotations

from asyncio import Future, ensure_future
from typing import TYPE_CHECKING

import pydantic

if TYPE_CHECKING:
    from psycopg import AsyncConnection


_cache: dict[str, Event] = {}
_cache_refresh: Future[dict[str, Event]] | None = None


class Event(pydantic.BaseModel):
    id: int
    slug: str
    name: str

    @classmethod
    async def get_event_by_slug(cls, db: AsyncConnection, slug: str) -> Event | None:
        cache = _cache
        if cache is None or slug not in cache:
            cache = await cls._refresh_cache(db)

        return cache.get(slug)

    @classmethod
    async def _refresh_cache(cls, db: AsyncConnection) -> dict[str, Event]:
        global _cache_refresh  # noqa: PLW0603
        if _cache_refresh is None:
            _cache_refresh = ensure_future(cls._do_refresh_cache(db))

        return await _cache_refresh

    @classmethod
    async def _do_refresh_cache(cls, db: AsyncConnection):
        async with db.cursor() as cursor:
            await cursor.execute("select id, slug, name from core_event")

            _cache.clear()
            async for id, slug, name in cursor:
                _cache[slug] = cls(id=id, slug=slug, name=name)

        return _cache
