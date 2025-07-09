from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import ClassVar
from uuid import UUID

import pydantic
from psycopg import AsyncConnection
from psycopg.errors import NotNullViolation

from graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGE_CODES

from ...optimized_server.utils.uuid7 import uuid7, uuid7_to_datetime
from ..config import KOMPASSI_V2_BASE_URL
from ..excs import InvalidProducts, UnsaneSituation
from ..utils.formatting import format_order_number, order_number_to_reference
from .customer import Customer
from .enums import PaymentStatus
from .ticket import reserve_tickets


class CreateOrderResult(pydantic.BaseModel):
    order_id: UUID
    order_number: int
    total_price: Decimal
    status: PaymentStatus

    @property
    def timestamp(self):
        return uuid7_to_datetime(self.order_id)

    @property
    def reference(self):
        return order_number_to_reference(self.timestamp, self.order_number)


class CreateOrderRequest(pydantic.BaseModel):
    customer: Customer
    products: dict[int, int]
    language: str

    query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "create_order.sql").read_bytes()

    @pydantic.field_validator("language", mode="before")
    @staticmethod
    def validate_language(value: str):
        if value not in SUPPORTED_LANGUAGE_CODES:
            return DEFAULT_LANGUAGE
        return value

    @pydantic.field_validator("products", mode="after")
    @staticmethod
    def validate_products(value: dict[int, int]):
        """
        Negative quantities are not allowed.
        """
        if any(quantity < 0 for quantity in value.values()):
            raise InvalidProducts()
        return value

    async def save(self, db: AsyncConnection, event_id: int):
        """
        Create order and reserve tickets.
        Must be called within a transaction (SELECT FOR UPDATE SKIP LOCKED).
        """
        async with db.cursor() as cursor:
            try:
                await cursor.execute(
                    self.query,
                    (
                        uuid7(),
                        event_id,
                        json.dumps(self.products),
                        self.language,
                        self.customer.first_name,
                        self.customer.last_name,
                        self.customer.email,
                        self.customer.phone,
                    ),
                )
            except NotNullViolation as e:
                raise InvalidProducts() from e

            if cursor.rowcount != 1:
                raise UnsaneSituation()

            (row,) = await cursor.fetchall()
            event_id_, order_id, total_price, order_number = row

            if event_id_ != event_id:
                raise UnsaneSituation()

        await reserve_tickets(db, event_id, order_id, self.products)

        return CreateOrderResult(
            order_id=order_id,
            order_number=order_number,
            total_price=total_price,
            status=PaymentStatus.PENDING if total_price else PaymentStatus.PAID,
        )


class OrderProduct(pydantic.BaseModel):
    title: str
    price: Decimal
    quantity: int


class Order(pydantic.BaseModel, populate_by_name=True):
    id: UUID
    order_number: int = pydantic.Field(
        serialization_alias="orderNumber",
        validation_alias="orderNumber",
    )
    status: PaymentStatus
    total_price: Decimal = pydantic.Field(
        serialization_alias="totalPrice",
        validation_alias="totalPrice",
    )
    language: str
    products: list[OrderProduct]

    query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "get_order.sql").read_bytes()

    @pydantic.computed_field(alias="formattedOrderNumber")
    @property
    def formatted_order_number(self) -> str:
        return format_order_number(self.order_number)

    @pydantic.computed_field(alias="createdAt")
    @property
    def created_at(self) -> datetime:
        return uuid7_to_datetime(self.id)

    @pydantic.field_serializer("status")
    def serialize_status(self, value: PaymentStatus):
        return value.name

    @pydantic.field_validator("status", mode="before")
    @staticmethod
    def validate_status(value: str | int | PaymentStatus):
        if isinstance(value, str):
            return PaymentStatus[value]
        else:
            return PaymentStatus(value)

    @classmethod
    async def get(cls, db: AsyncConnection, event_id: int, order_id: UUID) -> Order | None:
        async with db.cursor() as cursor:
            await cursor.execute(cls.query, dict(event_id=event_id, order_id=order_id))

            order_products = []
            total_price = Decimal(0)
            status = PaymentStatus.NOT_STARTED
            order_number = 0
            language_ = ""

            async for total_, order_number_, language_, title, price, quantity, status_ in cursor:
                order_products.append(OrderProduct(title=title, price=price, quantity=quantity))
                total_price, order_number, language, status = total_, order_number_, language_, status_

            if not order_products:
                return None

            return cls(
                id=order_id,
                total_price=total_price,
                language=language,
                status=status,
                order_number=order_number,
                products=order_products,
            )

    @property
    def reference(self):
        return order_number_to_reference(self.created_at, self.order_number)

    def get_url(self, event_slug: str):
        return f"{KOMPASSI_V2_BASE_URL}/{event_slug}/orders/{self.id}"


class OrderWithCustomer(Order):
    customer: Customer

    query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "get_order_with_customer.sql").read_bytes()

    @classmethod
    async def get(cls, db: AsyncConnection, event_id: int, order_id: UUID) -> OrderWithCustomer | None:
        async with db.cursor() as cursor:
            await cursor.execute(cls.query, dict(event_id=event_id, order_id=order_id))

            order_products = []
            total_price = Decimal(0)
            language = ""
            status = PaymentStatus.NOT_STARTED
            order_number = 0
            first_name = ""
            last_name = ""
            email = ""
            phone = ""

            # TODO dehorriblen this
            async for (
                total_,
                order_number_,
                language_,
                title,
                price,
                quantity,
                status_,
                first_name_,
                last_name_,
                email_,
                phone_,
            ) in cursor:
                order_products.append(OrderProduct(title=title, price=price, quantity=quantity))
                total_price, order_number, language, status = total_, order_number_, language_, status_
                first_name, last_name, email, phone = first_name_, last_name_, email_, phone_

            if not order_products:
                return None

            return cls(
                id=order_id,
                total_price=total_price,
                language=language,
                status=status,
                order_number=order_number,
                products=order_products,
                customer=Customer(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                ),
            )
