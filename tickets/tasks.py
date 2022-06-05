from celery import shared_task


@shared_task(ignore_result=True)
def batch_send_delivery_confirmation_messages(batch_id):
    from .models import Batch

    batch = Batch.objects.get(pk=batch_id)
    batch._send_delivery_confirmation_messages()


@shared_task(ignore_result=True)
def order_send_confirmation_message(order_id, msgtype):
    from .models import Order

    order = Order.objects.get(pk=order_id)
    order._send_confirmation_message(msgtype)
