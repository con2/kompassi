"""
usage: python manage.py tickets_v2_worker

A worker that sends receipts.
The worker is notified via `notify tickets_v2_server` in Postgres.
In the absence of such notifications, the worker will poll the database every NOTIFY_TIMEOUT_SECONDS.
When roused, the worker will process all pending receipts and then go back to sleep.
"""

import logging

from django.db import transaction
from psycopg import connect

from .models.receipts import Receipt, ReceiptStamp, ReceiptStampType, ReceiptStatus
from .optimized_server.db import get_conninfo

logger = logging.getLogger("kompassi")
NOTIFY_TIMEOUT_SECONDS = 300  # this is how often the worker will execute no matter what


def tick():
    logger.debug("Tick.")

    # Mark orders as being processed
    with transaction.atomic():
        # TODO If we ever add multiple workers, we need to make sure that each worker gets a different set of orders.
        # This could be via SELECT … FOR UPDATE SKIP LOCKED on the orders table, or via a parent process distributing work.
        # TODO If we had uuid_generate_v7() in the database, this could be done in an INSERT … SELECT.
        items, have_more_work = Receipt.get_pending_receipts()
        ReceiptStamp.objects.bulk_create(
            ReceiptStamp(
                order_id=item.order_id,
                event_id=item.event_id,
                correlation_id=item.correlation_id,
                type=ReceiptStampType.ORDER_CONFIRMATION,
                status=ReceiptStatus.PROCESSING,
            )
            for item in items
        )

    if not items:
        logger.debug("Tock. (No receipts to send)")
        return have_more_work

    logger.info("Sending receipts for %s orders.", len(items))

    # NOTE: if we ever add multiple workers, need to have KeyboardInterrupt write ReceiptStatus.FAILURE for unprocessed items

    # Process the orders
    for item in items:
        try:
            item.send_receipt()
        except RuntimeError as e:
            logger.error("Failed to send receipt for order %s", item.order_id, exc_info=e)
            ReceiptStamp(
                order_id=item.order_id,
                event_id=item.event_id,
                correlation_id=item.correlation_id,
                type=ReceiptStampType.ORDER_CONFIRMATION,
                status=ReceiptStatus.FAILURE,
            ).save()
        else:
            ReceiptStamp(
                order_id=item.order_id,
                event_id=item.event_id,
                correlation_id=item.correlation_id,
                type=ReceiptStampType.ORDER_CONFIRMATION,
                status=ReceiptStatus.SUCCESS,
            ).save()

    logger.debug("Tock.")

    return have_more_work


def run():
    # this connection is only used for notifies
    with connect(get_conninfo(), autocommit=True) as conn:
        logger.info("Connected to database")

        with conn.cursor() as cursor:
            cursor.execute("listen tickets_v2_order")
        logger.info("Listening for notifications on tickets_v2_order")

        while True:
            # process all work that is currently available
            while tick():
                pass

            # wait for up to NOTIFY_TIMEOUT_SECONDS for a notification
            for _ in conn.notifies(timeout=NOTIFY_TIMEOUT_SECONDS, stop_after=1):
                pass

            # clear the remaining notifications currently queued
            # there is one per order but we process orders in a batch
            for _ in conn.notifies(timeout=0):
                pass


if __name__ == "__main__":
    raise SystemError("Please run the worker through python manage.py tickets_v2_worker for now.")
