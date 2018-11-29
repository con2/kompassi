# encoding: utf-8

import hashlib

from django.conf import settings
from django.db import models

from core.models import EventMetaBase

from .defaults import EVENT_META_DEFAULTS
from .utils import u


class PaymentsEventMeta(EventMetaBase):
    checkout_password = models.CharField(max_length=255)
    checkout_merchant = models.CharField(max_length=255)
    checkout_delivery_date = models.CharField(max_length=9)

    @classmethod
    def get_or_create_dummy(cls, event=None):
        from django.contrib.auth.models import Group
        from core.models import Event

        if event is None:
            event, unused = Event.get_or_create_dummy()

        group, = PaymentsEventMeta.get_or_create_groups(event, ['admins'])

        return cls.objects.get_or_create(event=event, defaults=dict(
            EVENT_META_DEFAULTS,
            admin_group=group,
        ))

    class Meta:
        verbose_name = 'tapahtuman maksunvälitystiedot'
        verbose_name_plural = 'tapahtuman maksunvälitystiedot'


class Payment(models.Model):
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE)

    # XXX What the fuck is this and why the fuck is it here
    test = models.IntegerField(blank=True, null=True)

    VERSION = models.CharField(max_length=4)
    STAMP = models.CharField(max_length=20)
    REFERENCE = models.CharField(max_length=20)
    PAYMENT = models.CharField(max_length=20)
    STATUS = models.IntegerField()
    ALGORITHM = models.IntegerField()
    MAC = models.CharField(max_length=32)

    def _check_mac(self):
        meta = self.event.payments_event_meta
        assert meta is not None

        computed_mac = hashlib.md5()
        computed_mac.update(u(meta.checkout_password))
        computed_mac.update(b'&')
        computed_mac.update(u(self.VERSION))
        computed_mac.update(b'&')
        computed_mac.update(u(self.STAMP))
        computed_mac.update(b'&')
        computed_mac.update(u(self.REFERENCE))
        computed_mac.update(b'&')
        computed_mac.update(u(self.PAYMENT))
        computed_mac.update(b'&')
        computed_mac.update(u(str(self.STATUS)))
        computed_mac.update(b'&')
        computed_mac.update(u(str(self.ALGORITHM)))

        return self.MAC == computed_mac.hexdigest().upper()

    def clean(self):
        if not self._check_mac():
            from django.core.exceptions import ValidationError
            raise ValidationError('MAC does not match')
