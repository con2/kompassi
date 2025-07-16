"""
Contains Django versions of the functions that are used in optimized_server to create orders.
These functions are used for the admin GraphQL API.
They call the same SQL queries but instead of an async psycopg3 connection,
they use a Django connection.

NOTE: As an important difference, these functions do not honor the available_from/available_until
fields of the products. This is by design so as to allow the admin to create orders
containing products that are not available for public sale at the moment.

However, these functions _will_ still honor product quotas and will _not_ allow
creating orders that would exceed the available quota for a product.

These functions will also not perform such extensive caching as the optimized_server
versions do, as they are not expected to be called frequently.
"""

from __future__ import annotations

import json
from pathlib import Path

from django.db import IntegrityError, connection

from core.models.event import Event
from graphql_api.language import DEFAULT_LANGUAGE

from ..models.order import Order
from ..optimized_server.excs import InvalidProducts, NotEnoughTickets, UnsaneSituation
from ..optimized_server.models.customer import Customer
from ..optimized_server.models.order import ProductsDict, validate_products_dict
from ..optimized_server.utils.uuid7 import uuid7

OPTIMIZED_SERVER_SQL_DIR = Path(__file__).parent.parent / "optimized_server" / "models" / "sql"
CREATE_ORDER_QUERY = (OPTIMIZED_SERVER_SQL_DIR / "create_order.sql").read_text()


def create_order(
    event: Event,
    customer: Customer,
    products: ProductsDict,
    language: str = DEFAULT_LANGUAGE,
):
    """
    Preferred way to create orders from Django code.
    NOTE: Must be called within a transaction (uses SELECT FOR UPDATE SKIP LOCKED).
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                CREATE_ORDER_QUERY,
                (
                    uuid7(),
                    event.id,
                    json.dumps(products),
                    language,
                    customer.first_name,
                    customer.last_name,
                    customer.email,
                    customer.phone,
                ),
            )
        except IntegrityError as e:
            raise InvalidProducts() from e

        if cursor.rowcount != 1:
            raise UnsaneSituation()

        (row,) = cursor.fetchall()
        event_id_, order_id, _total_price, _order_number = row

        if event_id_ != event.id:
            raise UnsaneSituation()

    order = Order.objects.get(event_id=event.id, id=order_id)
    reserve_tickets(order)

    return order


RESERVE_TICKETS_QUERY = (OPTIMIZED_SERVER_SQL_DIR / "reserve_tickets.sql").read_text()


def reserve_tickets(order: Order):
    """
    Given an order and a dictionary of product id -> quantity, tries to reserve as many
    tickets to that order.

    Either succeeds and returns those tickets, or raises a NotEnoughTickets.
    The caller must rollback on NotEnoughTickets.
    Must be called in a transaction.
    """
    products = validate_products_dict(order.product_data)

    # quota_id -> quantity
    expected_tickets = get_expected_tickets_for_products(order.event_id, products)

    with connection.cursor() as cursor:
        cursor.execute(
            RESERVE_TICKETS_QUERY,
            dict(
                event_id=order.event_id,
                order_id=order.id,
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
        for row in cursor:
            _id, row_event_id, quota_id, row_order_id = row

            if row_event_id != order.event_id:
                raise UnsaneSituation()

            if row_order_id != order.id:
                raise UnsaneSituation()

            actual_tickets.setdefault(quota_id, 0)
            actual_tickets[quota_id] += 1

    if actual_tickets != expected_tickets:
        raise NotEnoughTickets()


def get_expected_tickets_for_products(
    event_id: int,
    products: ProductsDict,
) -> dict[int, int]:
    """
    Given a dictionary of product id -> quantity, returns a dictionary of quota id -> quantity.
    """
    quota_ids_by_product_id = get_quota_ids_by_product_id(event_id)
    print("quota_ids_by_product_id", quota_ids_by_product_id)
    print("products", products)

    expected_quantities_by_quota_id: dict[int, int] = {}
    for product_id, quantity in products.items():
        for quota_id in quota_ids_by_product_id[product_id]:
            expected_quantities_by_quota_id.setdefault(quota_id, 0)
            expected_quantities_by_quota_id[quota_id] += quantity

    return expected_quantities_by_quota_id


QUOTA_IDS_QUERY = (OPTIMIZED_SERVER_SQL_DIR / "get_quota_ids_by_product_id.sql").read_text()


def get_quota_ids_by_product_id(event_id: int) -> dict[int, list[int]]:
    """
    Get a mapping of product id -> [quota id, ...] of available products.
    """

    with connection.cursor() as cursor:
        cursor.execute(QUOTA_IDS_QUERY, [event_id])
        return dict(cursor.fetchall())
