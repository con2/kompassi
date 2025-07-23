from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from psycopg import AsyncConnection


get_quota_ids_by_product_id_query = (Path(__file__).parent / "sql" / "get_quota_ids_by_product_id.sql").read_bytes()


async def get_quota_ids_by_product_id(db: AsyncConnection, event_id: int) -> dict[int, list[int]]:
    """
    Get a mapping of product id -> [quota id, ...] of available products.

    NOTE: This is on the Hot Path, so be careful with performance.
    """

    async with db.cursor() as cursor:
        await cursor.execute(get_quota_ids_by_product_id_query, [event_id])
        return dict(await cursor.fetchall())


def get_quota_ids_by_product_id_django(event_id: int) -> dict[int, list[int]]:
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute(get_quota_ids_by_product_id_query.decode(), [event_id])
        return dict(cursor.fetchall())


# (event_id, (product_id, quantity)...) -> {quota_id: quantity}
_cache: dict[tuple[int, tuple[tuple[int, int], ...]], dict[int, int]] = {}


async def get_expected_tickets_for_products(
    aconn: AsyncConnection,
    event_id: int,
    products: dict[int, int],
) -> dict[int, int]:
    """
    Given a dictionary of product id -> quantity, returns a dictionary of quota id -> quantity.
    """
    cache_key = (event_id, tuple(sorted(products.items())))
    if cache_key in _cache:
        return _cache[cache_key]

    quota_ids_by_product_id = await get_quota_ids_by_product_id(aconn, event_id)

    expected_quantities_by_quota_id: dict[int, int] = {}
    for product_id, quantity in products.items():
        for quota_id in quota_ids_by_product_id[product_id]:
            expected_quantities_by_quota_id.setdefault(quota_id, 0)
            expected_quantities_by_quota_id[quota_id] += quantity

    _cache[cache_key] = expected_quantities_by_quota_id

    return expected_quantities_by_quota_id
