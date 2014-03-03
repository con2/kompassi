# encoding: utf-8

from django.db import models
from django.template import Template, Context
from django.utils import timezone


class Message(models.Model):
    event = models.ForeignKey('core.Event')
    app_label = models.CharField(max_length=63)
    recipient_group = models.ForeignKey('auth.Group')

    subject_template = models.CharField(max_length=255)
    body_template = models.TextField()

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
                person_message.actually_send_email()

    @classmethod
    def send_messages(cls, event, app_label, person):
        for message in Message.objects.filter(
            event=event,
            app_label=app_label,
            sent_at__isnull=False,
            expired_at__isnull=True,
            recipient_group__in=person.user.groups.all(),
        ):
            message.send(recipients=[person,], resend=False)

    @property
    def app_event_meta(self):
        return self.event.app_event_meta(self.app_label)


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
        self.subject, unused = PersonMessageSubject.get_or_create(self.render_message(self.message.subject_template))
        self.body, unused = PersonMessageBody.get_or_create(self.render_message(self.message.body_template))

        return super(PersonMessage, self).save(*args, **kwargs)

    @property
    def message_vars(self):
        if not hasattr(self, '_message_vars'):
            self._message_vars = dict(
                event=self.message.event,
                person=self.person,

                # TODO need a way to make app-specific vars
                #signup=Signup.objects.get(event=self.message.event, person=self.person),
            )

        return self._message_vars

    def render_message(self, template):
        return Template(template).render(Context(self.message_vars))

    def actually_send_email(self):
        from django.core.mail import EmailMessage

        msgbcc = []
        meta = self.message.app_event_meta

        if meta.monitor_email:
            msgbcc.append(meta.monitor_email)

        EmailMessage(
            subject=self.subject.text,
            body=self.body.text,
            from_email=meta.contact_email,
            to=(self.person.name_and_email,),
            bcc=msgbcc
        ).send(fail_silently=True)
