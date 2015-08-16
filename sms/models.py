# encoding: utf-8

from datetime import datetime

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.template import Template, Context
from django.utils import timezone
from nexmo.models import InboundMessage, OutboundMessage, message_received
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
                    category = VoteCategories.objects.get(value_min__lte=match.group('vote'),  value_max__gte=match.group('vote'), mapped=found)
                except VoteCategories.DoesNotExist:
                    # Ok,  there was none,  or vote value out of scope, vote rejected.
                    vote = "rejected"
                except VoteCategories.MultipleObjectsReturned:
                    # Value error or multiple categories with overlapping values. Saving to first one.
                    category = VoteCategories.objects.filter(value_min__lte=match.group('vote'),  value_max__gte=match.group('vote'), mapped=found)
                    existing_vote = Vote.objects.filter(hotword=found, category=category[0], voter=message.sender)
                    if(len(existing_vote) == 0):
                        # no old vote, adding new
                        vote = Vote(hotword=found, category=category[0], vote=match.group('vote'),  voter=message.sender, message=message)
                        vote.save()
                    else:
                        existing_vote[0].vote = match.group('vote')
                        existing_vote[0].message = message
                        existing_vote[0].save()
                else:
                    # There WAS category. Saving into it.
                    existing_vote = Vote.objects.filter(hotword=found, category=category, voter=message.sender)
                    if(len(existing_vote) == 0):
                        # no old vote, adding new
                        vote = Vote(hotword=found, category=category, vote=match.group('vote'),  voter=message.sender, message=message)
                        vote.save()
                    else:
                        existing_vote[0].vote = match.group('vote')
                        existing_vote[0].message = message
                        existing_vote[0].save()

            else:
                categories = VoteCategories.objects.filter(value_min__lte=match.group('vote'),  value_max__gte=match.group('vote'), mapped=found)
                saved = False
                for category in categories:
                    if category.slug == match.group('category'):
                        existing_vote = Vote.objects.filter(hotword=found, category=category, voter=message.sender)
                        if(len(existing_vote) == 0):
                            # no old vote, adding new
                            vote = Vote(hotword=found, category=category, vote=match.group('vote'),  voter=message.sender, message=message)
                            vote.save()
                        else:
                            existing_vote[0].vote = match.group('vote')
                            existing_vote[0].message = message
                            existing_vote[0].save()
                        saved = True
                if saved is False:
                    if len(categories) == 1:
                        # Wrong category,  but only one found. Saving there.
                        existing_vote = Vote.objects.filter(hotword=found, category=categories, voter=message.sender)
                        if(len(existing_vote) == 0):
                            # no old vote, adding new
                            vote = Vote(hotword=found, category=categories, vote=match.group('vote'),  voter=message.sender, message=message)
                            vote.save()
                        else:
                            existing_vote[0].vote = match.group('vote')
                            existing_vote[0].message = message
                            existing_vote[0].save()
                    #else:
                        # Value error, vote value out of scope or wrong category entered and multiple categories with overlapping values. Not saving
        # else:
            # Voting message with non-valid hotword.
            # It is very unlikely to someone start their message with "I am 13" or something like it (word [word] digit)
    else:
        #regular message with no hotword.
        try:
            event = SMSEvent.objects.get(current=True, sms_enabled=True)
        except SMSEvent.DoesNotExist:
            # Don't know to which event point the new message, ignored.
            pass
        else:
            new_message = SMSMessageIn(message=message, smsevent=event)
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


class VoteCategories(models.Model):
    category = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        max_length=20
    )
    mapped = models.ForeignKey(Hotword)
    value_min = models.IntegerField()
    value_max = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.category)

    class Meta:
        verbose_name = u'Kategoria'
        verbose_name_plural = u'Kategoriat'


class Vote(models.Model):
    hotword = models.ForeignKey(Hotword)
    category = models.ForeignKey(VoteCategories)
    vote = models.IntegerField()
    voter = models.CharField(
        max_length=30
    )
    message = models.ForeignKey('nexmo.InboundMessage')

    class Meta:
        verbose_name = u'Ääni'
        verbose_name_plural = u'Äänet'


class SMSEvent(models.Model):
    event = models.ForeignKey('core.Event')
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
                temp = SMSEvent.objects.get(current=True)
                if self != temp:
                    temp.current = False
                    temp.save()
            except SMSEvent.DoesNotExist:
                pass
        return super(SMSEvent, self).save(*args, **kwargs)

    @property
    def is_sms_enabled(self):
        return self.sms_enabled is not None
    
    @property
    def is_current(self):
        return self.current is not None
    
    def __unicode__(self):
        return self.event

    class Meta:
        verbose_name = u'Tekstiviestejä käyttävä tapahtuma'
        verbose_name_plural = u'Tekstiviestejä käyttävät tapahtumat'


class SMSMessageIn(models.Model):
    message = models.ForeignKey('nexmo.InboundMessage')
    smsevent = models.ForeignKey(SMSEvent)

    class Meta:
        verbose_name = u'Vastaanotettu viesti'
        verbose_name_plural = u'Vastaanotetut viestit'


class SMSMessageOut(models.Model):
    message = models.TextField()
    to = models.CharField(
        max_length=20
    )
    event = models.ForeignKey(SMSEvent)
    ref = models.ForeignKey('nexmo.OutboundMessage')

    @classmethod
    def send(cls, *args, **kwargs):
        event = SMSEvent.get(event=cls.event)
        to = regex.match(r'\d{9,15}', cls.to.replace(' ','').replace('-','').replace('+',''))
        if to is not None:
            if to[0].startswith('0'):
                actual_to = u'+358'.join(to[0][1:])
            else:
                actual_to = u'+'.join(to[0])
            nexmo_message = OutboundMessage(message=cls.message, to=actual_to)
            nexmo_message.save()
            out_message = SMSMessageOut(message=cls.message, to=actual_to, event=event, ref=nexmo_message)
            out_message.save()
            return out_message._send()
        else:
            return False

    def _send(self, *args, **kwargs):
        from time import sleep
        if self.ref is None:
            nexmo_message = OutboundMessage(message=self.message, to=self.to)
            nexmo_message.save()
            self.ref = nexmo_message
            self.save()

        sent_message = self.ref._send()

        for sent in sent_message['messages']
            price = sent['message-price'] * 100
            self.event.used_credit += price

        self.save()

        i = 1
        for i <= sent_message['message-count']
            sleep(0.2)
            i += 1

    class Meta:
        verbose_name = u'Lähetetty viesti'
        verbose_name_plural = u'Lähetetyt viestit'
