import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


def get_conninfo():
    return f"""
    dbname={os.getenv("POSTGRES_DATABASE", "kompassi")}
    user={os.getenv("POSTGRES_USERNAME", "kompassi")}
    password={os.getenv("POSTGRES_PASSWORD", "secret")}
    host={os.getenv("POSTGRES_HOSTNAME", "localhost")}
    port={os.getenv("POSTGRES_PORT", "5432")}
    """


def get_pool_size() -> tuple[int, int | None]:
    """
    Defaults (4, None -> effectively 4) reproduce psycopg_pool's own defaults, so leaving
    TICKETS_V2_POOL_MIN_SIZE/TICKETS_V2_POOL_MAX_SIZE unset changes nothing.
    """
    min_size_raw = os.getenv("TICKETS_V2_POOL_MIN_SIZE")
    max_size_raw = os.getenv("TICKETS_V2_POOL_MAX_SIZE")
    min_size = int(min_size_raw) if min_size_raw else 4
    max_size = int(max_size_raw) if max_size_raw else None
    return min_size, max_size


_pool: AsyncConnectionPool | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _pool  # noqa: PLW0603

    min_size, max_size = get_pool_size()
    logger.info("Starting connection pool with min_size=%s, max_size=%s", min_size, max_size)

    async with AsyncConnectionPool(get_conninfo(), min_size=min_size, max_size=max_size) as pool:
        _pool = pool  # type: ignore
        yield
        _pool = None


def get_connection_pool() -> AsyncConnectionPool:
    if _pool is None:
        raise RuntimeError("connection pool not initialised (lifespan not entered)")
    return _pool


async def db() -> AsyncIterator[AsyncConnection]:
    async with _pool.connection() as conn:  # type: ignore
        yield conn


DB = Annotated[AsyncConnection, Depends(db)]
