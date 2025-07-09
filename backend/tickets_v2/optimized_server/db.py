import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool


def get_conninfo():
    return f"""
    dbname={os.getenv('POSTGRES_DATABASE', 'kompassi')}
    user={os.getenv('POSTGRES_USERNAME', 'kompassi')}
    password={os.getenv('POSTGRES_PASSWORD', 'secret')}
    host={os.getenv('POSTGRES_HOSTNAME', 'localhost')}
    port={os.getenv('POSTGRES_PORT', '5432')}
    """


_pool: AsyncConnectionPool | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _pool  # noqa: PLW0603

    async with AsyncConnectionPool(get_conninfo()) as pool:
        _pool = pool  # type: ignore
        yield
        _pool = None


async def db() -> AsyncIterator[AsyncConnection]:
    async with _pool.connection() as conn:  # type: ignore
        yield conn


DB = Annotated[AsyncConnection, Depends(db)]
