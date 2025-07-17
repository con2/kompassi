import logging
from datetime import datetime
from hashlib import sha1

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template import Context, Template
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from labour.models import JobCategory, PersonnelClass

logger = logging.getLogger("kompassi")
APP_LABEL_CHOICES = [
    ("labour", "Työvoima"),
    ("programme", "Ohjelma"),
]


class RecipientGroup(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, verbose_name="Tapahtuma")
    app_label = models.CharField(max_length=63, choices=APP_LABEL_CHOICES, verbose_name="Sovellus")
    group = models.ForeignKey("auth.Group", on_delete=models.CASCADE, verbose_name="Käyttäjäryhmä")
    verbose_name = models.CharField(max_length=255, verbose_name="Nimi", blank=True, default="")
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, null=True, blank=True)
    programme_category = models.ForeignKey("programme.Category", on_delete=models.CASCADE, null=True, blank=True)
    programme_form = models.ForeignKey(
        "programme.AlternativeProgrammeForm", on_delete=models.CASCADE, null=True, blank=True
    )
    personnel_class = models.ForeignKey(PersonnelClass, on_delete=models.CASCADE, null=True, blank=True)
    override_reply_to = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Reply-to address"),
        help_text=_(
            "Due to spam protection, the sender field will always display a technical address "
            "in the kompassi.eu domain. That address will redirect incoming mail to the default "
            "contact address. You can direct replies to another address by setting a reply-to address here. "
            "Format: foo@example.com or Foo Bar &lt;foo@example.com&gt;."
        ),
    )

    def __str__(self):
        num_ppl = self.group.user_set.count() if self.group else "–"

        if self.job_category:
            kind = f" (tehtäväalue, {num_ppl} hlö)"
        elif self.personnel_class:
            kind = f" (henkilöstöluokka, {num_ppl} hlö)"
        elif self.programme_category:
            kind = f" (ohjelmaluokka, {num_ppl} hlö)"
        elif self.programme_form:
            kind = f" (ohjelmalomake, {num_ppl} hlö)"
        else:
            kind = f" ({num_ppl} hlö)"

        return f"{self.event.name}: {self.verbose_name}{kind}"

    class Meta:
        verbose_name = "vastaanottajaryhmä"
        verbose_name_plural = "vastaanottajaryhmät"


CHANNEL_CHOICES = [
    ("email", "Sähköposti"),
    # ("sms", "Tekstiviesti"),
]


@receiver(pre_save, sender=RecipientGroup)
def set_recipient_group_computed_fields(sender, instance, **kwargs):
    if not instance.verbose_name:
        if instance.job_category:
            instance.verbose_name = instance.job_category.name
        elif instance.personnel_class:
            instance.verbose_name = instance.personnel_class.name


@receiver(post_save, sender=JobCategory)
def update_jc_recipient_group_verbose_name(sender, instance, created, **kwargs):
    if created:
        return

    RecipientGroup.objects.filter(job_category=instance).update(verbose_name=instance.name)


@receiver(post_save, sender=PersonnelClass)
def update_pc_recipient_group_verbose_name(sender, instance, created, **kwargs):
    if created:
        return

    RecipientGroup.objects.filter(personnel_class=instance).update(verbose_name=instance.name)


class Message(models.Model):
    channel = models.CharField(
        max_length=5,
        verbose_name="Kanava",
        default="email",
        choices=CHANNEL_CHOICES,
    )
    recipient = models.ForeignKey(RecipientGroup, on_delete=models.CASCADE, verbose_name="Vastaanottajaryhmä")

    subject_template = models.CharField(
        max_length=255,
        verbose_name="Otsikko",
        help_text="HUOM! Otsikko näkyy vastaanottajalle ainoastaan, jos viesti lähetetään "
        "sähköpostitse. Tekstiviestillä lähetettäville viesteille otsikkoa käytetään "
        "ainoastaan viestin tunnistamiseen sisäisesti.",
    )
    body_template = models.TextField(
        verbose_name="Viestin teksti",
        help_text="Teksti {{ signup.formatted_job_categories_accepted }} korvataan "
        "listalla hyväksytyn vänkärin tehtäväalueista ja teksti "
        "{{ signup.formatted_shifts }} korvataan vänkärin vuoroilla. "
        "Käyttäessäsi näitä muotoilukoodeja laita ne omiksi kappaleikseen ts. reunusta ne tyhjillä riveillä.",
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

    @property
    def reply_to(self):
        # if self.override_reply_to:
        #     return self.override_reply_to
        if self.recipient and self.recipient.override_reply_to:
            return self.recipient.override_reply_to
        else:
            return None

    def send(self, recipients=None, resend=False):
        from .tasks import message_send

        if not self.sent_at:
            self.sent_at = timezone.now()
            self.save()

        message_send.delay(self.pk, [person.pk for person in recipients] if recipients is not None else None, resend)  # type: ignore

    def _send(self, recipients, resend):
        if recipients is None:
            recipients = [user.person for user in self.recipient.group.user_set.all()]

        for person in recipients:
            try:
                person_message, created = PersonMessage.objects.get_or_create(
                    person=person,
                    message=self,
                )
            except PersonMessage.MultipleObjectsReturned:
                # This actually happens sometimes.
                logger.warning("A Person doth multiple PersonMessages for a single Message have!")
                person_message = PersonMessage.objects.filter(person=person, message=self).first()
                created = False

            if not person_message:
                raise AssertionError("This won't happen (appease typechecker)")

            if created or resend:
                person_message.actually_send()

    def expire(self):
        if self.expired_at is not None:
            raise AssertionError("re-expiring an expired message does not make sense")
        if self.sent_at is None:
            raise AssertionError("expiring an unsent message does not make sense")

        self.expired_at = datetime.now()
        self.save()

    def unexpire(self):
        if not self.expired_at is not None:
            raise AssertionError("cannot un-expire a non-expired message")

        self.expired_at = None
        self.save()

        # Send to those that have been added to recipients while the message was expired
        self.send()

    @classmethod
    def send_messages(cls, event, app_label, person):
        for message in Message.objects.filter(
            recipient__app_label=app_label,
            recipient__event=event,
            recipient__group__in=person.user.groups.all(),
            sent_at__isnull=False,
            expired_at__isnull=True,
        ):
            message.send(
                recipients=[
                    person,
                ],
                resend=False,
            )

    @property
    def event(self):
        return self.recipient.event

    @property
    def app_label(self):
        return self.recipient.app_label

    @property
    def app_event_meta(self):
        return self.event.get_app_event_meta(self.app_label)

    def __str__(self):
        return Template(self.subject_template).render(Context(dict(event=self.event)))

    class Meta:
        verbose_name = "viesti"
        verbose_name_plural = "viestit"


class DedupMixin:
    @classmethod
    def get_or_create(cls, text):
        the_hash = sha1(text.encode("UTF-8")).hexdigest()

        try:
            return cls.objects.get_or_create(  # type: ignore
                digest=the_hash,
                defaults=dict(
                    text=text,
                ),
            )
        except cls.MultipleObjectsReturned:  # type: ignore
            logger.warning("Multiple %s returned for hash %s", cls.__name__, the_hash)
            return cls.objects.filter(digest=the_hash, text=text).first(), False  # type: ignore


class PersonMessageSubject(models.Model, DedupMixin):
    digest = models.CharField(max_length=63, db_index=True)
    text = models.CharField(max_length=255)


class PersonMessageBody(models.Model, DedupMixin):
    digest = models.CharField(max_length=63, db_index=True)
    text = models.TextField()


class PersonMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    person = models.ForeignKey("core.Person", on_delete=models.CASCADE)

    # dedup
    subject = models.ForeignKey(PersonMessageSubject, on_delete=models.CASCADE)
    body = models.ForeignKey(PersonMessageBody, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.subject, unused = PersonMessageSubject.get_or_create(self.render_message(self.message.subject_template))
        self.body, unused = PersonMessageBody.get_or_create(self.render_message(self.message.body_template))

        return super().save(*args, **kwargs)

    @property
    def message_vars(self):
        if not hasattr(self, "_message_vars"):
            self._message_vars = dict(
                event=self.message.event,
                person=self.person,
            )

            # TODO need a way to make app-specific vars in the apps themselves
            if "labour" in settings.INSTALLED_APPS:
                from labour.models import Signup

                try:
                    signup = Signup.objects.get(event=self.message.event, person=self.person)
                except Signup.DoesNotExist:
                    signup = None

                self._message_vars.update(signup=signup)

        return self._message_vars

    def render_message(self, template):
        return Template(template).render(Context(self.message_vars))

    def actually_send(self):
        from django.core.mail import EmailMessage

        msgbcc = []
        meta = self.message.app_event_meta

        if meta.monitor_email:
            msgbcc.append(meta.monitor_email)

        if settings.DEBUG:
            print(self.body.text)

        reply_to_tup = (reply_to_str,) if (reply_to_str := self.message.reply_to) else None

        EmailMessage(
            subject=self.subject.text,
            body=self.body.text,
            from_email=meta.cloaked_contact_email,
            to=(self.person.name_and_email,),
            bcc=msgbcc,
            reply_to=reply_to_tup,
        ).send(fail_silently=True)
