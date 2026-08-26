from __future__ import annotations

import logging

from .models.order import Order

logger = logging.getLogger(__name__)


def tickets_v2_cron_nightly():
    logger.info("Running nightly tasks for tickets_v2")
    Order.cancel_unpaid_orders()


def tickets_v2_cron_frequent():
    logger.info("Running frequent tasks for tickets_v2")
    Order.cancel_unpaid_orders()
    Order.retry_paid_after_cancellation()


if __name__ == "__main__":
    raise NotImplementedError("Use python manage.py cron_nightly or cron_frequent instead.")
