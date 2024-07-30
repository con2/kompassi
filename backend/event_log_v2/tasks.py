from celery import shared_task

from .models import Entry, Subscription


@shared_task(ignore_result=True)
def subscription_send_update_for_entry(subscription_id, entry_id):
    subscription = Subscription.objects.get(id=subscription_id)
    entry = Entry.objects.get(id=entry_id)

    subscription._send_update_for_entry(entry)
