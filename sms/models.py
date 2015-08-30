# encoding: utf-8

from datetime import datetime

from django.conf import settings
from django.db import models, connection
from django.dispatch import receiver
from django.template import Template, Context
from django.utils import timezone
from nexmo.models import InboundMessage, OutboundMessage, message_received
from core.models import EventMetaBase
import regex

APP_LABEL_CHOICES = [
    ('labour', 'Työvoima')
]


@receiver(message_received)
def sms_received_handler(sender, **kwargs):
    messages = InboundMessage.objects.filter(nexmo_message_id=kwargs['nexmo_message_id'])
    message = messages[0]  # If nexmo has delivered same message multiple times.
    now = timezone.now()
    hotwords = Hotword.objects.filter(valid_from__lte=now, valid_to__gte=now)
    match = regex.match(r'(?P<hotword>[a-z]+) ((?P<category>[a-z]*)(?:\s?)(?P<vote>\d+))', message.message.lower())  # doesn't work with pythons re. Recursive patterns are not allowed.
    if match is not None:
        # Message with hotword
        for hotword in hotwords:
            found = False
            if hotword.slug == match.group('hotword'):
                found = hotword
                break
        if found is not False:
            # Valid hotword found, check category.
            if match.group('category') == '':
                # no category, checking if there should be
                try:
                    nominee = Nominee.objects.get(number=int(match.group('vote')), category__hotword=found)
                except Nominee.DoesNotExist:
                    # Ok,  there was none,  or vote value out of scope, vote rejected.
                    vote = "rejected"
                except Nominee.MultipleObjectsReturned:
                    try:
                        nominee = Nominee.objects.get(number=match.group('vote'), category__primary=True, category__hotword=found)
                    except Nominee.DoesNotExist:
                        vote = "rejected"
                    else:
                        try:
                            category = VoteCategory.objects.get(nominee=nominee,primary=True)
                            existing_vote = Vote.objects.get(message__sender=message.sender,category=category)
                        except Vote.DoesNotExist:
                            # No old vote
                            vote = Vote(category=category,vote=nominee,message=message)
                            vote.save()
                        else:
                            existing_vote.vote = nominee
                            existing_vote.message = message
                            existing_vote.category = category
                            existing_vote.save()
                else:
                    try:
                        category = nominee.category.all()[0]
                        existing_vote = Vote.objects.get(message__sender=message.sender,category=category)
                    except Vote.DoesNotExist:
                        # No old vote
                        vote = Vote(category=category,vote=nominee,message=message)
                        vote.save()
                    else:
                        existing_vote.vote = nominee
                        existing_vote.message = message
                        existing_vote.category = category
                        existing_vote.save()

            else:
                try:
                    nominee = Nominee.objects.get(number=match.group('vote'), category__slug=match.group('category'), category__hotword=found)
                except Nominee.DoesNotExist:
                    vote = "rejected"
                else:
                    try:
                        category = VoteCategory.objects.get(slug=match.group('category'))
                        existing_vote = Vote.objects.get(message__sender=message.sender,vote=nominee)
                    except Vote.DoesNotExist:
                        # No old vote
                        vote = Vote(category=category,vote=nominee,message=message)
                        vote.save()
                    else:
                        existing_vote.vote = nominee
                        existing_vote.message = message
                        existing_vote.category = category
                        existing_vote.save()
        else:
            # Voting message with non-valid hotword.
            # It is very unlikely to someone start their message with "I am 13" or something like it (word [word] digit)
            # But hadle it anyway as regular message
            try:
                event = SMSEventMeta.objects.get(current=True, sms_enabled=True)
            except SMSEventMeta.DoesNotExist:
                # Don't know to which event point the new message, ignored.
                pass
            else:
                new_message = SMSMessageIn(message=message, SMSEventMeta=event)
                new_message.save()
    else:
        #regular message with no hotword.
        try:
            event = SMSEventMeta.objects.get(current=True, sms_enabled=True)
        except SMSEventMeta.DoesNotExist:
            # Don't know to which event point the new message, ignored.
            pass
        else:
            new_message = SMSMessageIn(message=message, SMSEventMeta=event)
            new_message.save()


class Hotword(models.Model):
    hotword = models.CharField(
        max_length=255,
        verbose_name=u"Hotwordin kuvaus",
        help_text=u"Tällä nimellä erotat hotwordin muista, esim. toisen tapahtuman AMV-äänestyksestä"
    )
    slug = models.SlugField(
        verbose_name=u"Avainsana",
        help_text=u"Tämä tekstinpätkä on varsinainen avainsana, joka tulee löytyä tekstiviestistä. Kirjoita pienillä!"
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    assigned_event = models.ForeignKey('core.Event')

    def __unicode__(self):
        return u'%s' % (self.hotword)

    class Meta:
        verbose_name = u'Hotwordi'
        verbose_name_plural = u'Hotwordit'


class VoteCategory(models.Model):
    category = models.CharField(
        max_length=255,
        verbose_name=u'Kategorian kuvaus'
    )
    slug = models.SlugField(
        max_length=20,
        verbose_name=u'Avainsana'
    )
    hotword = models.ForeignKey(Hotword)
    primary = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.category)

    class Meta:
        verbose_name = u'Kategoria'
        verbose_name_plural = u'Kategoriat'


class Nominee(models.Model):
    category = models.ManyToManyField(VoteCategory)
    number = models.IntegerField()
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return u'%s - %s' % (self.number, self.name)
    
    class Meta:
        verbose_name = u'Osallistuja'
        verbose_name_plural = u'Osallistujat'


class Vote(models.Model):
    category = models.ForeignKey(VoteCategory)
    vote = models.ForeignKey(Nominee)
    message = models.ForeignKey('nexmo.InboundMessage')

    class Meta:
        verbose_name = u'Ääni'
        verbose_name_plural = u'Äänet'


class SMSEventMeta(EventMetaBase):
    sms_enabled = models.BooleanField(
        default=False
    )
    current = models.BooleanField(
        default=False
    )
    used_credit = models.IntegerField(
        default=0
    )

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
    
    def __unicode__(self):
        return self.event.name
    
    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        group, unused = cls.get_or_create_group(event, 'admins')
        return cls.objects.get_or_create(event=event, defaults=dict(admin_group=group))

    class Meta:
        verbose_name = u'Tekstiviestejä käyttävä tapahtuma'
        verbose_name_plural = u'Tekstiviestejä käyttävät tapahtumat'


class SMSMessageIn(models.Model):
    message = models.ForeignKey('nexmo.InboundMessage')
    SMSEventMeta = models.ForeignKey(SMSEventMeta)

    def __unicode__(self):
        return self.message.message

    class Meta:
        verbose_name = u'Vastaanotettu viesti'
        verbose_name_plural = u'Vastaanotetut viestit'


class SMSMessageOut(models.Model):
    message = models.TextField()
    to = models.CharField(
        max_length=20
    )
    event = models.ForeignKey(SMSEventMeta)
    ref = models.ForeignKey('nexmo.OutboundMessage', blank=True, null=True)

    @classmethod
    def send(cls, *args, **kwargs):
        message = SMSMessageOut(*args, **kwargs)
        message.save()
        return message._send()

    def _send(self, *args, **kwargs):
        from time import sleep
        if self.event.sms_enabled:
            to = regex.match(r'\d{9,15}', self.to.replace(' ','').replace('-','').replace('+',''))
            if to is not None:
                if to[0].startswith('0'):
                    actual_to = u'+358' + to[0][1:]
                else:
                    actual_to = u'+' + to[0]
                nexmo_message = OutboundMessage(message=self.message, to=actual_to)
                nexmo_message.save()
                self.to = actual_to
                self.ref = nexmo_message
                self.save()

                not_throttled = 0
                while not_throttled == 0:
                    try:
                        sent_message = self.ref._send()
                    except nexmo.RetryError:
                        # Back off! Stop everything for a while.
                        sleep(0.4)
                    else:
                        not_throttled = 1

                event = SMSEventMeta.objects.get(event=self.event)
                for sent in sent_message['messages']:
                    if sent['status'] == 0:
                        price = float(sent['message-price']) * 100
                        event.used_credit += int(price)

                event.save()

                if 'background_tasks' in settings.INSTALLED_APPS:
                    # This assumes that if background_tasks is installed, it will be used in sms sending.
                    # Otherwise you will be hitting RetryError constantly.
                    pass
                else:
                    sleep(0.25 * float(sent_message['message-count']))

                return True
            else:
                return False
        else:
            return False

    class Meta:
        verbose_name = u'Lähetetty viesti'
        verbose_name_plural = u'Lähetetyt viestit'
