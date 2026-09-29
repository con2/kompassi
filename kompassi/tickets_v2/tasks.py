import logging

from django.db import transaction
from django.dispatch import receiver
from django.tasks import TaskResult, TaskResultStatus, task
from django.tasks.signals import task_finished

from .models.receipt import PendingReceipt, Receipt
from .optimized_server.models.enums import ReceiptStatus

logger = logging.getLogger(__name__)


@task(max_attempts=3)
def send_receipt(event_id: int, receipt_id: str):
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
        logger.info("Receipt is not pending, skipping", extra=dict(event_id=event_id, receipt_id=receipt_id))
        return

    PendingReceipt.get(event_id=event_id, receipt_id=receipt_id).send_receipt()

    Receipt.objects.filter(event_id=event_id, id=receipt_id).update(status=ReceiptStatus.SUCCESS)


@receiver(task_finished)
def mark_receipt_failed(sender, task_result: TaskResult, **kwargs):
    """
    Covers every way a send_receipt task can end in failure, including a worker
    dying mid-send and the task's lease expiring.
    """
    if task_result.task.module_path != send_receipt.module_path:
        return
    if task_result.status != TaskResultStatus.FAILED:
        return

    event_id, receipt_id = task_result.args
    Receipt.objects.filter(event_id=event_id, id=receipt_id, status=ReceiptStatus.PROCESSING).update(
        status=ReceiptStatus.FAILURE
    )
