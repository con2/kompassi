# encoding: utf-8



from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


TARGET_FKEY_ATTRS = dict(
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
)


class Entry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    entry_type = models.CharField(max_length=255)

    # various target fkeys, sparse
    feedback_message = models.ForeignKey('feedback.FeedbackMessage', **TARGET_FKEY_ATTRS)

    def send_updates(self):
        from .subscription import Subscription

        subscriptions = Subscription.objects.filter(entry_type=self.entry_type, active=True)
        for subscription in subscriptions:
            subscription.send_update_for_entry(self)

    @property
    def entry_type_metadata(self):
        if not hasattr(self, '_entry_type_metadata'):
            from .. import registry
            self._entry_type_metadata = registry.get(self.entry_type)

        return self._entry_type_metadata

    @property
    def email_reply_to(self):
        meta = self.entry_type_metadata

        if callable(meta.email_reply_to):
            return meta.email_reply_to(self)
        else:
            return meta.email_reply_to

    @property
    def message(self):
        meta = self.entry_type_metadata

        if callable(meta.message):
            return meta.message(self)
        else:
            return meta.message.format(entry=self)

    @property
    def email_subject(self):
        return '[{app_name}] {message}'.format(
            app_name=settings.KOMPASSI_INSTALLATION_NAME,
            message=self.message,
        )

    @property
    def email_body(self):
        meta = self.entry_type_metadata

        if callable(meta.email_body_template):
            return meta.email_body_template(self)
        else:
            return render_to_string(meta.email_body_template, dict(
                entry=self,
                settings=settings,
            ))

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        ordering = ('-created_at',)
