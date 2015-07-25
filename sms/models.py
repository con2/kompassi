# encoding: utf-8

from datetime import datetime

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.template import Template, Context
from django.utils import timezone
from nexmo.models import InboundMessage, message_received
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
            if hotword.hotword == match.group('hotword'):
                found = hotword
                break
        if found is not False:
            # Valid hotword found, check category.
            if match.group('category') == '':
                # no category, checking if there should be
                try:
                    category = VoteCategories.objects.get(value_min__lte=match.group('vote'),  value_max__gte=match.group('vote'), mapped=found)
                except VoteCategories.DoesNotExist:
                    # Ok,  there was none,  or vote value out of scope,  proceed.
                    empty_category = VoteCategories.get_or_create(category="Ei voittoa", category_slug="empty", value_min=0, value_max=0)
                    vote = Vote(hotword=found, category=empty_category, vote=match.group('vote'),  voter=message.sender)
                    vote.save()
                except VoteCategories.MultipleObjectsReturned:
                    # Value error or multiple categories with overlapping values. Saving to first one.
                    category = VoteCategories.objects.filter(value_min__lte=match.group('vote'),  value_max__gte=match.group('vote'), mapped=found)
                    vote = Vote(hotword=found, category=category[0], vote=match.group('vote'),  voter=message.sender)
                    vote.save()
                else:
                    # There WAS category. Saving into it.
                    existing_vote = Vote.objects.filter(hotword=found, category=category, voter=message.sender)
                    if(len(existing_vote) == 0):
                        # no old vote, adding new
                        vote = Vote(hotword=found, category=category, vote=match.group('vote'),  voter=message.sender)
                        vote.save()
                    else:
                        existing_vote[0].vote = match.group('vote')
                        existing_vote[0].save()

            else:
                categories = VoteCategories.objects.filter(value_min__lte=match.group('vote'),  value_max__gte=match.group('vote'), mapped=found)
                saved = False
                for category in categories:
                    if category.slug == match.group('category'):
                        existing_vote = Vote.objects.filter(hotword=found, category=category, voter=message.sender)
                        if(len(existing_vote) == 0):
                            # no old vote, adding new
                            vote = Vote(hotword=found, category=category, vote=match.group('vote'),  voter=message.sender)
                            vote.save()
                        else:
                            existing_vote[0].vote = match.group('vote')
                            existing_vote[0].save()
                        saved = True
                if saved is False:
                    if len(categories) == 1:
                        # Wrong category,  but only one found. Saving there.
                        existing_vote = Vote.objects.filter(hotword=found, category=categories, voter=message.sender)
                        if(len(existing_vote) == 0):
                            # no old vote, adding new
                            vote = Vote(hotword=found, category=categories, vote=match.group('vote'),  voter=message.sender)
                            vote.save()
                        else:
                            existing_vote[0].vote = match.group('vote')
                            existing_vote[0].save()
                    #else:
                        # Value error,  wrong category entered and multiple categories with overlapping values. Not saving
        # else:
            # Voting message with non-valid hotword.
    else:
        #regular message with no hotword.
        print "no hotword found"


class Hotword(models.Model):
    hotword = models.CharField(
        max_length=255
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
    slug = models.CharField(
        max_length=10
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

    class Meta:
        verbose_name = u'Ääni'
        verbose_name_plural = u'Äänet'


class SMSMessage(models.Model):
    recipient = models.ForeignKey('mailings.RecipientGroup', verbose_name=u'Vastaanottajaryhmä')

    body_template = models.TextField(
        verbose_name=u'Viestin teksti',
        help_text=u'Teksti {{ signup.formatted_job_categories_accepted }} korvataan '
            u'listalla hyväksytyn vänkärin tehtäväalueista ja teksti '
            u'{{ signup.formatted_shifts }} korvataan vänkärin vuoroilla.',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    expired_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_sent(self):
        return self.sent_at is not None

    @property
    def is_expired(self):
        return self.expired_at is not None

    def send(self, recipients=None, resend=False):
        if 'background_tasks' in settings.INSTALLED_APPS:
            from mailings.tasks import message_send
            message_send.delay(
                self.pk,
                [person.pk for person in recipients] if recipients is not None else None,
                resend
            )
        else:
            self._send(recipients, resend)

    def _send(self, recipients, resend):
        from django.contrib.auth.models import User

        if not self.sent_at:
            self.sent_at = timezone.now()
            self.save()

        if recipients is None:
            recipients = [user.person for user in self.recipient.group.user_set.all()]

        for person in recipients:
            person_message, created = PersonSMSMessage.objects.get_or_create(
                person=person,
                message=self,
            )

            if created or resend:
                person_message.actually_send_email()

    def expire(self):
        assert self.expired_at is None, 're-expiring an expired message does not make sense'
        assert self.sent_at is not None, 'expiring an unsent message does not make sense'

        self.expired_at = datetime.now()
        self.save()

    def unexpire(self):
        assert self.expired_at is not None, 'cannot un-expire a non-expired message'

        self.expired_at = None
        self.save()

        # Send to those that have been added to recipients while the message was expired
        self.send()

    @classmethod
    def send_messages(cls, event, app_label, person):
        for message in SMSMessage.objects.filter(
            recipient__app_label=app_label,
            recipient__event=event,
            recipient__group__in=person.user.groups.all(),
            sent_at__isnull=False,
            expired_at__isnull=True,
        ):
            message.send(recipients=[person,], resend=False)

    @property
    def event(self):
        return self.recipient.event

    @property
    def app_label(self):
        return self.recipient.app_label

    @property
    def app_event_meta(self):
        return self.event.app_event_meta(self.app_label)

    def __unicode__(self):
        return Template(self).render(Context(dict(event=self.event)))

    class Meta:
        verbose_name = u'Lähetetty viesti'
        verbose_name_plural = u'Lähetetyt viestit'


class DedupMixin(object):
    @classmethod
    def get_or_create(cls, text):
        from hashlib import sha1
        return cls.objects.get_or_create(
            digest=sha1(text.encode('UTF-8')).hexdigest(),
            defaults=dict(
                text=text,
            )
        )


class PersonSMSMessageBody(models.Model, DedupMixin):
    digest = models.CharField(max_length=63, db_index=True)
    text = models.TextField()


class PersonSMSMessage(models.Model):
    message = models.ForeignKey(SMSMessage)
    person = models.ForeignKey('core.Person')

    # dedup
    body = models.ForeignKey(PersonSMSMessageBody)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.body, unused = PersonSMSMessageBody.get_or_create(self.render_message(self.message.body_template))

        return super(PersonSMSMessage, self).save(*args, **kwargs)

    @property
    def message_vars(self):
        if not hasattr(self, '_message_vars'):
            self._message_vars = dict(
                event=self.message.event,
                person=self.person,
            )

            # TODO need a way to make app-specific vars in the apps themselves
            if 'labour' in settings.INSTALLED_APPS:
                from labour.models import Signup

                try:
                    signup = Signup.objects.get(event=self.message.event, person=self.person)
                except Signup.DoesNotExist:
                    signup = None

                self._message_vars.update(signup=signup)

        return self._message_vars

    def render_message(self, template):
        return Template(template).render(Context(self.message_vars))

    def actually_send_email(self):
        from nexmo import OutboundMessage

        if settings.DEBUG:
            print self.body.text

        OutboundMessage.send(
            message=self.body.text,
            to=(self.person.phone,),
        )
