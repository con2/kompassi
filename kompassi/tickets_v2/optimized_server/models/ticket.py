from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from ..excs import NotEnoughTickets, UnsaneSituation
from .quota import get_expected_tickets_for_products

if TYPE_CHECKING:
    from uuid import UUID

    from psycopg import AsyncConnection


# NOTE: bytes instead of str in order to placate typechecker
reserve_query = (Path(__file__).parent / "sql" / "reserve_tickets.sql").read_bytes()


async def reserve_tickets(
    db: AsyncConnection,
    event_id: int,
    order_id: UUID,
    products: dict[int, int],
):
    """
    Given an order and a dictionary of product id -> quantity, tries to reserve as many
    tickets to that order.

    Either succeeds and returns those tickets, or raises a NotEnoughTickets.
    The caller must rollback on NotEnoughTickets.
    Must be called in a transaction.

    NOTE: This is the hot path. Be very mindful of performance.
    """
    # quota_id -> quantity
    expected_tickets: dict[int, int] = await get_expected_tickets_for_products(db, event_id, products)

    async with db.cursor() as cursor:
        await cursor.execute(
            reserve_query,
            dict(
                event_id=event_id,
                order_id=order_id,
                quantities_by_quota_id=json.dumps(
                    [
                        {
                            "quota_id": quota_id,
                            "quantity": quantity,
                        }
                        for (quota_id, quantity) in expected_tickets.items()
                    ]
                ),
            ),
        )

        actual_tickets: dict[int, int] = {}
        async for row in cursor:
            _id, row_event_id, quota_id, row_order_id = row

            if row_event_id != event_id:
                raise UnsaneSituation()

            if row_order_id != order_id:
                raise UnsaneSituation()

            actual_tickets.setdefault(quota_id, 0)
            actual_tickets[quota_id] += 1

    if actual_tickets != expected_tickets:
        raise NotEnoughTickets()
