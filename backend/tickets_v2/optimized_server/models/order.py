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

    async def save(self, db: AsyncConnection, event_id: int):
        order_id = uuid7()
        customer_data = self.customer.model_dump(mode="json", by_alias=True)

        async with db.cursor() as cursor:
            try:
                await cursor.execute(
                    self.create_query,
                    dict(
                        order_id=order_id,
                        event_id=event_id,
                        product_data=json.dumps(self.products),
                        customer_data=json.dumps(customer_data),
                    ),
                )
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

        order_id = uuid7()
        customer_data = self.customer.model_dump(mode="json", by_alias=True)

        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    self.create_query.decode(),
                    dict(
                        order_id=order_id,
                        event_id=event_id,
                        product_data=json.dumps(self.products),
                        customer_data=json.dumps(customer_data),
                    ),
                )
            except NotNullViolation as e:
                raise InvalidProducts() from e

            if cursor.rowcount != 1:
                raise UnsaneSituation()

            (row,) = cursor.fetchall()
            event_id, order_id = row

        reserve_tickets_django(event_id, order_id, self.products)

        return order_id
