"""
Customer self-service cancellation eligibility.

This is the single source of truth for the cancellation deadline arithmetic
and the eligibility rule. It is used by three layers that each fetch the
inputs differently:

- kompassi.tickets_v2.models.order.Order (GraphQL mutations, authoritative)
- kompassi.tickets_v2.models.receipt.PendingReceipt (receipt emails)
- kompassi.tickets_v2.optimized_server.models.order.Order (anonymous order API)

NOTE: Must remain free of Django imports (used by the optimized server).
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
from decimal import Decimal

from ..models.enums import PaymentStatus


def get_cancellation_deadline(
    order_created_at: datetime,
    cancellation_period_days: int,
    event_start_time: datetime | None,
) -> datetime | None:
    """
    Deadline for customer self-service cancellation, or None if disabled.
    The cancellation period starts at order creation and is capped at event start.
    """
    if not cancellation_period_days:
        return None

    deadline = order_created_at + timedelta(days=cancellation_period_days)

    if event_start_time is not None:
        deadline = min(deadline, event_start_time)

    return deadline


def get_payment_deadline(
    order_created_at: datetime,
    unpaid_order_cancellation_delay_minutes: int,
) -> datetime | None:
    """
    Deadline by which an unpaid order must be paid before the automatic
    cancellation sweep cancels it, or None when the event has automatic
    cancellation of unpaid orders disabled (delay_minutes == 0) and there is
    therefore no deadline to show the customer.
    """
    if not unpaid_order_cancellation_delay_minutes:
        return None

    return order_created_at + timedelta(minutes=unpaid_order_cancellation_delay_minutes)


def is_cancellable_by_customer(
    *,
    status: PaymentStatus,
    cancellation_deadline: datetime | None,
    now: datetime,
    total_price: Decimal,
    is_paid_by_provider: Callable[[], bool],
) -> bool:
    """
    Customer self-service cancellation (confirmed via email) is allowed for paid
    orders within the cancellation period, provided that any money paid can be
    automatically refunded via the payment provider. Customers holding orders
    that fail these criteria are directed to contact ticket sales instead.

    is_paid_by_provider is a callable so that callers backed by a database
    query only pay for it when the cheaper criteria have already passed.
    """
    if status != PaymentStatus.PAID:
        return False

    if cancellation_deadline is None or now >= cancellation_deadline:
        return False

    return total_price == 0 or is_paid_by_provider()
