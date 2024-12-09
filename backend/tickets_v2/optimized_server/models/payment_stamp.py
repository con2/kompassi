from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar, Self
from uuid import UUID

import pydantic
from psycopg import AsyncConnection

from tickets_v2.optimized_server.utils.uuid7 import uuid7

from .enums import PaymentProvider, PaymentStampType, PaymentStatus
from .event import Event


class PaymentStamp(pydantic.BaseModel):
    event_id: int
    order_id: UUID
    provider: PaymentProvider
    type: PaymentStampType
    status: PaymentStatus
    correlation_id: UUID
    data: dict[str, Any]

    create_query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "create_payment_stamp.sql").read_bytes()

    async def save(self, db: AsyncConnection) -> Self:
        async with db.cursor() as cursor:
            await cursor.execute(
                self.create_query,
                (
                    uuid7(),
                    self.event_id,
                    self.order_id,
                    self.provider.value,
                    self.type.value,
                    self.status.value,
                    self.correlation_id,
                    json.dumps(self.data),
                ),
            )

        return self

    @classmethod
    async def save_many(cls, db: AsyncConnection, stamps: list[PaymentStamp]):
        async with db.cursor() as cursor:
            await cursor.executemany(
                cls.create_query,
                [
                    (
                        uuid7(),
                        stamp.event_id,
                        stamp.order_id,
                        stamp.provider.value,
                        stamp.type.value,
                        stamp.status.value,
                        stamp.correlation_id,
                        json.dumps(stamp.data),
                    )
                    for stamp in stamps
                ],
            )

    @classmethod
    def for_zero_price_order(
        cls,
        event: Event,
        order_id: UUID,
    ) -> PaymentStamp:
        return cls(
            event_id=event.id,
            order_id=order_id,
            provider=event.provider,
            type=PaymentStampType.ZERO_PRICE,
            status=PaymentStatus.PAID,
            correlation_id=uuid7(),
            data={},
        )
