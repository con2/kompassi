from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Self

import pydantic

if TYPE_CHECKING:
    from psycopg import AsyncConnection


class Product(pydantic.BaseModel, populate_by_name=True):
    id: int
    title: str
    description: str
    price: Decimal
    max_per_order: int = pydantic.Field(
        validation_alias="maxPerOrder",
        serialization_alias="maxPerOrder",
    )
    available: bool | None

    list_query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "list_products.sql").read_bytes()

    @classmethod
    async def get_products(cls, aconn: AsyncConnection, event_id: int) -> list[Self]:
        async with aconn.cursor() as cursor:
            await cursor.execute(cls.list_query, dict(event_id=event_id))

            products = []
            async for row in cursor:
                id, title, description, price, max_per_order, available = row
                products.append(
                    cls(
                        id=id,
                        title=title,
                        description=description,
                        price=price,
                        max_per_order=max_per_order,
                        available=available,
                    )
                )

            return products
