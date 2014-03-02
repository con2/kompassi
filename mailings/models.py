# encoding: utf-8

from django.utils import timezone
from django.db import models


class Message(models.Model):
    event = models.ForeignKey('core.Event')
    app_label = models.CharField(max_length=63)
    recipient_group = models.ForeignKey('auth.Group')

    subject_template = models.CharField(max_length=255)
    body_template = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(blank=True)
    expired_at = models.DateTimeField(blank=True)

    @property
    def is_sent(self):
        return self.sent_at is not None

    @property
    def is_expired(self):
        return self.expired_at is not None

    @property
    def send(self, recipients=None, resend=False):
        from django.contrib.auth.models import User

        if not self.sent_at:
            self.sent_at = timezone.now()
            self.save()

        if recipients is None:
            recipients = self.recipient_group.user_set.all()

        for person in recipients:
            if type(person) == User:
                try:
                    person = person.person
                except Person.DoesNotExist:
                    # XXX whine
                    continue
            else:
                person = person

            person_message, created = PersonMessage.objects.get_or_create(
                person=person,
                message=self,
            )

            if created or resend:
                person_message.send()


class DedupMixin(object):
    @classmethod
    def get_or_create(cls, text):
        from hashlib import sha1
        return cls.objects.get_or_create(
            digest=sha1(text).hexdigest(),
            defaults=dict(
                text=text,
            )
        )


class PersonMessageSubject(models.Model, DedupMixin):
    digest = models.CharField(max_length=63, db_index=True)
    text = models.CharField(max_length=255)


class PersonMessageBody(models.Model, DedupMixin):
    digest = models.CharField(max_length=63, db_index=True)
    text = models.TextField()


class PersonMessage(models.Model):
    message = models.ForeignKey(Message)
    person = models.ForeignKey('core.Person')

    # dedup
    subject = models.ForeignKey(PersonMessageSubject)
    body = models.ForeignKey(PersonMessageBody)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.subject:
            self.subject, unused = PersonMessageSubject.get_or_create(self.render_subject())

        if not self.body:
            self.body, unused = PersonMessageText.get_or_create(self.render_body())

        return super(PersonMessage, self).save(*args, **kwargs)

    @property
    def message_vars(self):
        if not hasattr(self, '_message_vars'):
            self._message_vars = dict(
                event=event,
                person=person,
                signup=Signup.objects.get(event=event, person=person),
            )

        return self._message_vars

    def render_message(self):
        return render_to_string(self.message.body_template, self.message_vars)

    def render_subject(self):
        return render_to_string(self.message.subject_template, self.message_vars)

    def send(self):
        from django.core.mail import EmailMessage

        msgbcc = []

        if self.event.labour_event_meta.monitor_email:
            msgbcc.append(self.event.labour_event_meta.monitor_email)

        EmailMessage(
            subject=self.subject.text,
            body=self.body.text,
            from_email=self.event.labour_event_meta.contact_email,
            to=(self.customer.name_and_email,),
            bcc=msgbcc
        ).send(fail_silently=True)