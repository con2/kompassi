from __future__ import annotations

import logging

from .models.order import Order

logger = logging.getLogger("kompassi")


def tickets_v2_cron_nightly():
    logger.info("Running nightly tasks for tickets_v2")
    Order.cancel_unpaid_orders()


if __name__ == "__main__":
    raise NotImplementedError("Use python manage.py cron_nightly instead.")
