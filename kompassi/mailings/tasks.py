from django.tasks import task


@task
def message_send(message_id, recipient_ids=None, resend=False):
    from kompassi.core.models import Person

    from .models import Message

    message = Message.objects.get(pk=message_id)
    if recipient_ids is None:
        recipients = None
    else:
        recipients = Person.objects.filter(pk__in=recipient_ids)

    message._send(recipients, resend)
