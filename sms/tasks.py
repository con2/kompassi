from __future__ import absolute_import

from celery import shared_task


@shared_task(ignore_result=True)
def message_send(message, to, event):
    from .models import SMSMessageOut

    SMSMessageOut.send(message=message, to=to, event=event)
