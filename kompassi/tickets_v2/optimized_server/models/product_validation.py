from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

from ..excs import InvalidProducts

if TYPE_CHECKING:
    from psycopg import AsyncConnection

validate_products_query = (Path(__file__).parent / "sql" / "get_products_for_validation.sql").read_bytes()


class ProductValidationRow(NamedTuple):
    superseded_by_id: int | None
    available_from: datetime | None
    available_until: datetime | None


def _check_products(
    products: dict[int, int],
    rows: dict[int, ProductValidationRow],
    *,
    enforce_availability: bool,
    now: datetime,
) -> None:
    if not any(quantity > 0 for quantity in products.values()):
        raise InvalidProducts("Order must contain at least one product with a positive quantity.")

    for product_id in products:
        row = rows.get(product_id)
        if row is None:
            raise InvalidProducts(f"Product {product_id} does not belong to this event.")

        if row.superseded_by_id is not None:
            raise InvalidProducts(f"Product {product_id} has been superseded.")

        if enforce_availability and not (
            row.available_from is not None
            and row.available_from <= now
            and (row.available_until is None or now < row.available_until)
        ):
            raise InvalidProducts(f"Product {product_id} is not currently on sale.")


async def validate_products(db: AsyncConnection, event_id: int, products: dict[int, int]) -> None:
    """
    Public order creation policy: every product must belong to the event, be the
    current (non-superseded) version, and be within its availability window.

    NOTE: Keep in sync with validate_products_django.
    """
    async with db.cursor() as cursor:
        await cursor.execute(validate_products_query, dict(event_id=event_id, product_ids=list(products)))
        rows = {
            product_id: ProductValidationRow(superseded_by_id, available_from, available_until)
            for product_id, superseded_by_id, available_from, available_until in await cursor.fetchall()
        }

    _check_products(products, rows, enforce_availability=True, now=datetime.now(UTC))


def validate_products_django(event_id: int, products: dict[int, int]) -> None:
    """
    Admin order creation policy: every product must belong to the event and be the
    current (non-superseded) version. Unlike the public policy, the availability
    window is not enforced, so admins can create orders for products that are not
    currently on public sale.

    NOTE: Keep in sync with validate_products.
    """
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute(validate_products_query.decode(), dict(event_id=event_id, product_ids=list(products)))
        rows = {
            product_id: ProductValidationRow(superseded_by_id, available_from, available_until)
            for product_id, superseded_by_id, available_from, available_until in cursor.fetchall()
        }

    _check_products(products, rows, enforce_availability=False, now=datetime.now(UTC))
