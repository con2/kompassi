from __future__ import annotations

import json
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import ClassVar
from uuid import UUID

import pydantic
from psycopg import AsyncConnection
from psycopg.errors import NotNullViolation

from event_log_v2.utils.uuid7 import uuid7

from ..excs import InvalidProducts, UnsaneSituation
from .customer import Customer
from .ticket import reserve_tickets


class CreateOrderRequest(pydantic.BaseModel):
    customer: Customer
    products: dict[int, int]

    query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "create_order.sql").read_bytes()

    def get_params(self, event_id: int):
        return (
            uuid7(),
            event_id,
            json.dumps(self.products),
            self.customer.first_name,
            self.customer.last_name,
            self.customer.email,
            self.customer.phone,
        )

    async def save(self, db: AsyncConnection, event_id: int):
        async with db.cursor() as cursor:
            try:
                await cursor.execute(self.query, self.get_params(event_id))
            except NotNullViolation as e:
                raise InvalidProducts() from e

            if cursor.rowcount != 1:
                raise UnsaneSituation()

            (row,) = await cursor.fetchall()
            event_id, order_id = row

        await reserve_tickets(db, event_id, order_id, self.products)

        return order_id


class OrderStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class OrderProduct(pydantic.BaseModel):
    title: str
    price: Decimal
    quantity: int


class Order(pydantic.BaseModel):
    id: UUID
    products: list[OrderProduct]
    total: Decimal
    status: OrderStatus

    query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "get_order.sql").read_bytes()

    @classmethod
    async def get_order(cls, db: AsyncConnection, event_id: int, order_id: UUID) -> Order | None:
        async with db.cursor() as cursor:
            await cursor.execute(cls.query, dict(event_id=event_id, order_id=order_id))

            order_products = []
            total = Decimal(0)
            status = OrderStatus.CONFIRMED

            async for total_, title, price, quantity, status_ in cursor:
                order_products.append(OrderProduct(title=title, price=price, quantity=quantity))
                total, status = total_, status_

            if not order_products:
                return None

            return cls(
                id=order_id,
                products=order_products,
                total=total,
                status=status,
            )
