from celery import shared_task


@shared_task(ignore_result=True)
def order_send_confirmation_message(order_id: int, msgtype: str):
    from .models import Order

    order = Order.objects.get(pk=order_id)
    order._send_confirmation_message(msgtype)
