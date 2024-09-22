from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Self

import pydantic

if TYPE_CHECKING:
    from psycopg import AsyncConnection


class Product(pydantic.BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    available: bool

    list_query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "list_products.sql").read_bytes()

    @classmethod
    async def get_products(cls, aconn: AsyncConnection, event_id: int) -> list[Self]:
        async with aconn.cursor() as cursor:
            await cursor.execute(cls.list_query, dict(event_id=event_id))

            products = []
            async for row in cursor:
                id, title, description, price, available = row
                products.append(
                    cls(
                        id=id,
                        title=title,
                        description=description,
                        price=price,
                        available=available,
                    )
                )

            return products

    @classmethod
    def get_products_django(cls, event_id: int) -> list[Self]:
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(cls.list_query.decode(), dict(event_id=event_id))

            products = []
            for row in cursor:
                id, title, description, price, available = row
                products.append(
                    cls(
                        id=id,
                        title=title,
                        description=description,
                        price=price,
                        available=available,
                    )
                )

            return products
