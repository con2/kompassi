from __future__ import annotations

from asyncio import Future, ensure_future
from typing import TYPE_CHECKING, ClassVar

import pydantic

if TYPE_CHECKING:
    from psycopg import AsyncConnection


class Event(pydantic.BaseModel):
    id: int
    slug: str
    name: str

    cache: ClassVar[dict[str, Event]] = {}
    cache_refresh: ClassVar[Future[dict[str, Event]] | None] = None

    @classmethod
    async def get_event_by_slug(cls, db: AsyncConnection, slug: str) -> Event | None:
        if cls.cache is None or slug not in cls.cache:
            cls.cache = await cls._refresh_cache(db)

        return cls.cache.get(slug)

    @classmethod
    async def _refresh_cache(cls, db: AsyncConnection) -> dict[str, Event]:
        """
        Ensure only one refresh is running at a time.
        """
        if cls.cache_refresh is None:
            cls.cache_refresh = ensure_future(cls._do_refresh_cache(db))

        return await cls.cache_refresh

    @classmethod
    async def _do_refresh_cache(cls, db: AsyncConnection):
        """
        Actually refresh the cache.
        """
        async with db.cursor() as cursor:
            await cursor.execute("select id, slug, name from core_event")

            cls.cache.clear()
            async for id, slug, name in cursor:
                cls.cache[slug] = cls(id=id, slug=slug, name=name)

        return cls.cache
