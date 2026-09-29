from django.tasks import task

from .models import Entry, Subscription


@task
def subscription_send_update_for_entry(subscription_id: int, entry_id: str):
    subscription = Subscription.objects.get(id=subscription_id)
    entry = Entry.objects.get(id=entry_id)

    subscription._send_update_for_entry(entry)
