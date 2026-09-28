import logging

from django.db import transaction
from django.tasks import TaskContext, task

from .models.receipt import PendingReceipt, Receipt
from .optimized_server.models.enums import ReceiptStatus

logger = logging.getLogger(__name__)


@task(max_attempts=3, takes_context=True)
def send_receipt(context: TaskContext, event_id: int, receipt_id: str):
    """
    Enqueued by the notify_requested trigger on tickets_v2_receipt whenever a receipt
    row is inserted or updated with status REQUESTED.
    """
    with transaction.atomic():
        claimed = (
            Receipt.objects.filter(
                event_id=event_id,
                id=receipt_id,
                status__in=[ReceiptStatus.REQUESTED, ReceiptStatus.PROCESSING],
            )
            .select_for_update()
            .update(status=ReceiptStatus.PROCESSING)
        )

    if not claimed:
        logger.info("Receipt %s of event %s is not pending, skipping", receipt_id, event_id)
        return

    pending_receipt = PendingReceipt.get(event_id=event_id, receipt_id=receipt_id)

    try:
        pending_receipt.send_receipt()
    except Exception:
        task_result = context.task_result
        if task_result.attempts >= task_result.task.max_attempts:  # type: ignore[attr-defined]
            Receipt.objects.filter(event_id=event_id, id=receipt_id).update(status=ReceiptStatus.FAILURE)
        raise

    Receipt.objects.filter(event_id=event_id, id=receipt_id).update(status=ReceiptStatus.SUCCESS)
