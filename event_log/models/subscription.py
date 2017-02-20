# encoding: utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..channels import channels


CHANNEL_CHOICES = [
    ('email', _('E-mail')),
    # ('sms', _('SMS')),
    # ('push', _('Push notifications')),
]


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    entry_type = models.CharField(max_length=255)
    channel = models.CharField(
        max_length=max(len(key) for (key, label) in CHANNEL_CHOICES),
        default='email',
        choices=CHANNEL_CHOICES,
    )
    active = models.BooleanField(default=True)

    def send_update_for_entry(self, entry):
        assert self.active

        if 'background_tasks' in settings.INSTALLED_APPS:
            from ..tasks import subscription_send_update_for_entry
            subscription_send_update_for_entry.delay(self.id, entry.id)
        else:
            self._send_update_for_entry(entry)

    def _send_update_for_entry(self, entry):
        channels[self.channel].send_update_for_entry(self, entry)

    @property
    def recipient_name_and_email(self):
        full_name = self.user.get_full_name()
        if full_name:
            return '{full_name} <{email}>'.format(
                full_name=full_name,
                email=self.user.email,
            )
        else:
            return self.user.email

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        index_together = [
            ('entry_type', 'active'),
        ]
