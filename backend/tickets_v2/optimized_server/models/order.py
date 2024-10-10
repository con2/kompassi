from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar

import pydantic
from psycopg import AsyncConnection
from psycopg.errors import NotNullViolation

from event_log_v2.utils.uuid7 import uuid7

from ..excs import InvalidProducts, UnsaneSituation
from .customer import Customer
from .ticket import reserve_tickets, reserve_tickets_django


class Order(pydantic.BaseModel):
    customer: Customer
    products: dict[int, int]

    create_query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "create_order.sql").read_bytes()

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
                await cursor.execute(self.create_query, self.get_params(event_id))
            except NotNullViolation as e:
                raise InvalidProducts() from e

            if cursor.rowcount != 1:
                raise UnsaneSituation()

            (row,) = await cursor.fetchall()
            event_id, order_id = row

        await reserve_tickets(db, event_id, order_id, self.products)

        return order_id

    def save_django(self, event_id: int):
        from django.db import connection

        with connection.cursor() as cursor:
            try:
                cursor.execute(self.create_query.decode(), self.get_params(event_id))
            except NotNullViolation as e:
                raise InvalidProducts() from e

            if cursor.rowcount != 1:
                raise UnsaneSituation()

            (row,) = cursor.fetchall()
            event_id, order_id = row

        reserve_tickets_django(event_id, order_id, self.products)

        return order_id
