"""
usage: python manage.py tickets_v2_worker

A worker that sends receipts.
The worker is notified via `notify tickets_v2_paymentstamp` in Postgres.
In the absence of such notifications, the worker will poll the database every NOTIFY_TIMEOUT_SECONDS.
When roused, the worker will process all pending receipts and then go back to sleep.
"""

import logging

from django.db import transaction
from psycopg import connect

from .models.meta import TicketsV2EventMeta
from .models.receipt import PendingReceipt, Receipt
from .optimized_server.db import get_conninfo
from .optimized_server.models.enums import ReceiptStatus

logger = logging.getLogger(__name__)
NOTIFY_TIMEOUT_SECONDS = 300  # this is how often the worker will execute no matter what


def tick(event_id: int):
    logger.debug("Processing receipts for event %s…", event_id)

    # Mark orders as being processed
    with transaction.atomic():
        # TODO If we had uuid_generate_v7() in the database, this could be done in an INSERT … SELECT.
        items, have_more_work = PendingReceipt.claim_pending_receipts(event_id=event_id)

    if not items:
        logger.debug("Done sending receipts for event %s. (None to send)", event_id)
        return have_more_work

    logger.info("Sending receipts for %s orders.", len(items))

    # Process the orders
    # TODO on interrupt, mark the rest as FAILED
    while items:
        item = items.pop()
        try:
            item.send_receipt()
        except Exception as e:
            logger.exception("Failed to send receipt for order %s", item.order_id, exc_info=e)
            Receipt.objects.filter(event_id=item.event_id, id=item.receipt_id).update(status=ReceiptStatus.FAILURE)
        else:
            Receipt.objects.filter(event_id=item.event_id, id=item.receipt_id).update(status=ReceiptStatus.SUCCESS)

    logger.debug("Done sending receipts for event %s.", event_id)

    return have_more_work


def run():
    # this connection is only used for notifies
    with connect(get_conninfo(), autocommit=True) as conn:
        logger.info("Connected to database")

        with conn.cursor() as cursor:
            cursor.execute("listen tickets_v2_receipt")
        logger.info("Listening for notifications on tickets_v2_receipt")

        event_ids = set(TicketsV2EventMeta.objects.all().values_list("event_id", flat=True))

        while True:
            # process all work that is currently available
            for event_id in event_ids:
                while tick(event_id):
                    pass

            event_ids.clear()

            # wait for up to NOTIFY_TIMEOUT_SECONDS for a notification
            for notification in conn.notifies(timeout=NOTIFY_TIMEOUT_SECONDS, stop_after=1):
                event_ids.add(int(notification.payload))

            # clear the remaining notifications currently queued
            # there is max one per order but we process orders in a batch
            # note that postgres has already dedup'd them within the same transaction
            # but we want to dedup them across transactions
            for notification in conn.notifies(timeout=0):
                event_ids.add(int(notification.payload))


if __name__ == "__main__":
    raise SystemError("Please run the worker through python manage.py tickets_v2_worker for now.")
