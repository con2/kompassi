

from celery import shared_task


@shared_task(ignore_result=True)
def message_send(message_id):
    from .models import SMSMessageOut

    smsmessage = SMSMessageOut.objects.get(pk=message_id)
    smsmessage._send()
