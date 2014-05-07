from __future__ import absolute_import

from celery import shared_task


@shared_task(ignore_result=True)
def batch_send_delivery_confirmation_messages(batch_id):
    from .models import Batch

    batch = Batch.objects.get(pk=batch_id)
    batch._send_delivery_confirmation_messages()