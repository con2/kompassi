# encoding: utf-8



from django.conf import settings
from django.core.mail import EmailMessage


def send_update_for_entry(subscription, entry):
    subject = entry.email_subject
    body = entry.email_body

    opts = dict(
        subject=subject,
        body=body,
        to=(subscription.recipient_name_and_email,),
        reply_to=entry.email_reply_to,
    )

    if settings.DEBUG:
        print(body.encode('UTF-8'))

    EmailMessage(**opts).send(fail_silently=False)
