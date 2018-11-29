# encoding: utf-8

from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import F

from nexmo.models import InboundMessage, OutboundMessage, RetryError
import regex

from core.models import EventMetaBase


MAX_TRIES = 20
RETRY_DELAY_SECONDS = 0.4


class Hotword(models.Model):
    hotword = models.CharField(
        max_length=255,
        verbose_name="Avainsanan kuvaus",
        help_text="Tällä nimellä erotat avainsanan muista, esim. toisen tapahtuman AMV-äänestyksestä"
    )
    slug = models.SlugField(
        verbose_name="Avainsana",
        help_text="Tämä tekstinpätkä on varsinainen avainsana, joka tulee löytyä tekstiviestistä. Kirjoita pienillä!"
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    assigned_event = models.ForeignKey('core.Event', on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.hotword)

    class Meta:
        verbose_name = 'Avainsana'
        verbose_name_plural = 'Avainsanat'


class VoteCategory(models.Model):
    category = models.CharField(
        max_length=255,
        verbose_name='Kategorian kuvaus'
    )
    slug = models.SlugField(
        max_length=20,
        verbose_name='Avainsana'
    )
    hotword = models.ForeignKey(Hotword, on_delete=models.CASCADE)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.category)

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategoriat'


class Nominee(models.Model):
    category = models.ManyToManyField(VoteCategory)
    number = models.IntegerField()
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return '%s - %s' % (self.number, self.name)

    class Meta:
        verbose_name = 'Osallistuja'
        verbose_name_plural = 'Osallistujat'


class Vote(models.Model):
    category = models.ForeignKey(VoteCategory, on_delete=models.CASCADE)
    vote = models.ForeignKey(Nominee, on_delete=models.CASCADE)
    message = models.ForeignKey('nexmo.InboundMessage', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ääni'
        verbose_name_plural = 'Äänet'


class SMSEventMeta(EventMetaBase):
    sms_enabled = models.BooleanField(default=False)
    current = models.BooleanField(default=False)
    used_credit = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.current:
            try:
                temp = SMSEventMeta.objects.get(current=True)
                if self != temp:
                    temp.current = False
                    temp.save()
            except SMSEventMeta.DoesNotExist:
                pass
        return super(SMSEventMeta, self).save(*args, **kwargs)

    @property
    def is_sms_enabled(self):
        return self.sms_enabled is not None

    @property
    def is_current(self):
        return self.current is not None

    def __str__(self):
        return self.event.name

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        group, unused = cls.get_or_create_groups(event, ['admins'])
        return cls.objects.get_or_create(event=event, defaults=dict(admin_group=group))

    class Meta:
        verbose_name = 'Tekstiviestejä käyttävä tapahtuma'
        verbose_name_plural = 'Tekstiviestejä käyttävät tapahtumat'


class SMSMessageIn(models.Model):
    message = models.ForeignKey('nexmo.InboundMessage', on_delete=models.CASCADE)
    SMSEventMeta = models.ForeignKey(SMSEventMeta, on_delete=models.CASCADE)

    def __str__(self):
        return self.message.message

    class Meta:
        verbose_name = 'Vastaanotettu viesti'
        verbose_name_plural = 'Vastaanotetut viestit'


class SMSMessageOut(models.Model):
    message = models.TextField()
    to = models.CharField(max_length=20)
    event = models.ForeignKey(SMSEventMeta, on_delete=models.CASCADE)
    ref = models.ForeignKey('nexmo.OutboundMessage', on_delete=models.CASCADE, blank=True, null=True)

    @classmethod
    def send(cls, *args, **kwargs):
        message = SMSMessageOut(*args, **kwargs)
        message.save()
        return message._send()

    def _send(self, *args, **kwargs):
        from time import sleep
        if not self.event.sms_enabled:
            return False

        # TODO replace this with a generic phone number normalization code (perhaps a library)
        to = regex.match(r'\d{9,15}', self.to.replace(' ','').replace('-','').replace('+',''))
        if to is None:
            return False
        if to[0].startswith('0'):
            actual_to = '+358' + to[0][1:]
        else:
            actual_to = '+' + to[0]

        nexmo_message = OutboundMessage(message=self.message, to=actual_to)
        nexmo_message.save()

        self.to = actual_to
        self.ref = nexmo_message
        self.save()

        succeeded = False
        for i in range(MAX_TRIES):
            try:
                sent_message = self.ref._send()
            except RetryError:
                # Back off! Stop everything for a while.
                sleep(RETRY_DELAY_SECONDS)
            else:
                succeeded = True
                break

        if not succeeded:
            raise RuntimeError('Max retries exceeded for SMSMessageOut(id={})'.format(self.id))

        used_credit = sum(
            float(sent['message-price']) * 100
            for sent in sent_message['messages']
            if int(sent['status']) == 0
        )

        meta = SMSEventMeta.objects.get(event=self.event.event)
        meta.used_credit = F('used_credit') + int(used_credit)
        meta.save()

        if 'background_tasks' in settings.INSTALLED_APPS:
            # This assumes that if background_tasks is installed, it will be used in sms sending.
            # Otherwise you will be hitting RetryError constantly.
            pass
        else:
            sleep(0.25 * float(sent_message['message-count']))

        return True

    class Meta:
        verbose_name = 'Lähetetty viesti'
        verbose_name_plural = 'Lähetetyt viestit'


from . import signal_handlers
