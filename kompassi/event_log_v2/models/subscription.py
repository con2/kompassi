import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string

from .entry import Entry

logger = logging.getLogger(__name__)


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return f"{self.user} ({self.entry_type})"

    def send_update_for_entry(self, entry: Entry):
        from ..tasks import subscription_send_update_for_entry

        subscription_send_update_for_entry.delay(self.id, entry.id)  # type: ignore

    def _send_update_for_entry(self, entry: Entry):
        if not self.user.is_active:
            logger.info("Not sending email to inactive user %r", self.user)
            return

        subject = self.get_email_subject(entry)
        body = self.get_email_body(entry)

        if settings.DEBUG:
            print(body.encode("UTF-8"))

        EmailMessage(
            subject=subject,
            body=body,
            to=(self.recipient_name_and_email,),
            reply_to=self.get_email_reply_to(entry),
        ).send(fail_silently=False)

    def get_email_subject(self, entry: Entry):
        return f"[{settings.KOMPASSI_INSTALLATION_NAME}] {entry.message}"

    def get_email_body(self, entry: Entry):
        meta = entry.meta

        if callable(meta.email_body_template):
            return meta.email_body_template(entry)
        elif meta.email_body_template is None:
            return entry.message
        else:
            return render_to_string(
                meta.email_body_template,
                entry.message_vars,
            )

    def get_email_reply_to(self, entry: Entry):
        meta = entry.meta

        if callable(meta.email_reply_to):
            return meta.email_reply_to(entry)
        else:
            return meta.email_reply_to

    @property
    def recipient_name_and_email(self):
        full_name = self.user.get_full_name()
        if full_name:
            return f"{full_name} <{self.user.email}>"
        else:
            return self.user.email
