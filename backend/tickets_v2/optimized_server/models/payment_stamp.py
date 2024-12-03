import json
from pathlib import Path
from typing import Any, ClassVar
from uuid import UUID

import pydantic
from psycopg import AsyncConnection

from tickets_v2.optimized_server.utils.uuid7 import uuid7

from .enums import PaymentProvider, PaymentStampType, PaymentStatus


class PaymentStamp(pydantic.BaseModel):
    event_id: int
    order_id: UUID
    provider: PaymentProvider
    type: PaymentStampType
    status: PaymentStatus
    correlation_id: UUID
    data: dict[str, Any]

    create_query: ClassVar[bytes] = (Path(__file__).parent / "sql" / "create_payment_stamp.sql").read_bytes()

    async def save(self, db: AsyncConnection):
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
