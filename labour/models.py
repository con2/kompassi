# encoding: utf-8

from datetime import date, datetime, timedelta

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now

from core.models import EventMetaBase
from core.utils import format_datetime, SLUG_FIELD_PARAMS


class LabourEventMeta(EventMetaBase):
    signup_extra_content_type = models.ForeignKey('contenttypes.ContentType')

    registration_opens = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'työvoimahaku alkaa'
    )

    registration_closes = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'työvoimahaku päättyy'
    )

    work_begins = models.DateTimeField(verbose_name=u'Ensimmäiset työvuorot alkavat')
    work_ends = models.DateTimeField(verbose_name=u'Viimeiset työvuorot päättyvät')

    monitor_email = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'tarkkailusähköposti',
        help_text=u'Kaikki työvoimajärjestelmän lähettämät sähköpostiviestit lähetetään myös '
            u'tähän osoitteeseen.',
    )

    accepted_group = models.ForeignKey('auth.Group',
        null=True,
        blank=True,
        verbose_name=u'Työvoimaan hyväksyttyjen ryhmä',
        help_text=u'Järjestelmä lisää kaikki työvoimaan hyväksytyt automaattisesti tähän '
            u'käyttäjäryhmään pääsynvalvontaa varten.',
        related_name='+',
    )

    class Meta:
        verbose_name = u'tapahtuman työvoimatiedot'
        verbose_name_plural = u'tapahtuman työvoimatiedot'

    def __unicode__(self):
        return self.event.name if self.event else 'None'

    @property
    def signup_extra_model(self):
        return self.signup_extra_content_type.model_class()

    @classmethod
    def events_registration_open(cls):
        from core.models import Event
        t = now()
        return Event.objects.filter(
            laboureventmeta__registration_opens__isnull=False,
            laboureventmeta__registration_opens__lte=t,
        ).exclude(
            laboureventmeta__registration_closes__isnull=False,
            laboureventmeta__registration_closes__lte=t,
        )

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        from django.contrib.auth.models import Group
        from django.contrib.contenttypes.models import ContentType

        event, unused = Event.get_or_create_dummy()
        group, unused = Group.objects.get_or_create(name='Dummy group')
        content_type = ContentType.objects.get_for_model(EmptySignupExtra)

        t = now()

        return cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=group,
                signup_extra_content_type=content_type,
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
                work_begins=event.start_time - timedelta(days=1),
                work_ends=event.end_time + timedelta(days=1),
            )
        )

    @property
    def is_registration_open(self):
        t = now()
        return self.registration_opens and self.registration_opens <= t and \
            not (self.registration_closes and self.registration_closes <= t)

    def is_person_signed_up(self, person):
        return Signup.objects.filter(person=person, event=self.event).exists()

    def get_signup_for_person(self, person):
        try:
            return Signup.objects.get(person=person, event=self.event)
        except Signup.DoesNotExist:
            return Signup(person=person, event=self.event)

    def is_user_admin(self, user):
        if not user.is_authenticated():
            return False

        if user.is_superuser:
            return True

        return user.groups.filter(pk=self.admin_group.pk).exists()

    @property
    def work_hours(self):
        from programme.utils import full_hours_between
        return full_hours_between(self.work_begins, self.work_ends)


class Qualification(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    name = models.CharField(max_length=63, verbose_name=u'pätevyyden nimi')
    description = models.TextField(blank=True, verbose_name=u'kuvaus')

    qualification_extra_content_type = models.ForeignKey('contenttypes.ContentType', null=True, blank=True)

    class Meta:
        verbose_name = u'pätevyys'
        verbose_name_plural = u'pätevyydet'

    def __unicode__(self):
        return self.name

    @property
    def qualification_extra_model(self):
        if self.qualification_extra_content_type:
            return self.qualification_extra_content_type.model_class()
        else:
            return None

    @classmethod
    def create_dummy(cls):
        return cls.objects.create(
            name='Dummy qualification'
        )


class PersonQualification(models.Model):
    person = models.ForeignKey('core.Person', verbose_name=u'henkilö')
    qualification = models.ForeignKey(Qualification, verbose_name=u'pätevyys')

    class Meta:
        verbose_name = u'pätevyyden haltija'
        verbose_name_plural=u'pätevyyden haltijat'

    def __unicode__(self):
        return self.qualification.name if self.qualification else 'None'

    @property
    def qualification_extra(self):
        if not self.qualification:
            return None

        QualificationExtra = self.qualification.qualification_extra_model
        if not QualificationExtra:
            return None

        try:
            return QualificationExtra.objects.get(personqualification=self)
        except QualificationExtra.DoesNotExist:
            return QualificationExtra(personqualification=self)


class QualificationExtraBase(models.Model):
    personqualification = models.OneToOneField(PersonQualification,
        related_name="+",
        primary_key=True)

    @classmethod
    def get_form_class(cls):
        raise NotImplemented(
            'Remember to override get_form_class in your QualificationExtra model'
        )

    class Meta:
        abstract = True


class JobCategory(models.Model):
    event = models.ForeignKey('core.Event', verbose_name=u'tapahtuma')

    name = models.CharField(max_length=63, verbose_name=u'tehtäväalueen nimi')

    description = models.TextField(
        verbose_name=u'tehtäväalueen kuvaus',
        help_text=u'Kuvaus näkyy hakijoille hakulomakkeella. Kerro ainakin, mikäli tehtävään tarvitaan erityisiä tietoja tai taitoja.'
    )

    public = models.BooleanField(
        default=True,
        verbose_name=u'avoimessa haussa',
        help_text=u'Tehtäviin, jotka eivät ole avoimessa haussa, voi hakea vain työvoimavastaavan lähettämällä hakulinkillä.'
    )

    required_qualifications = models.ManyToManyField(Qualification,
        blank=True,
        verbose_name=u'vaaditut pätevyydet'
    )

    class Meta:
        verbose_name = u'tehtäväalue'
        verbose_name_plural=u'tehtäväalueet'

    def __unicode__(self):
        return self.name


class WorkPeriod(models.Model):
    event = models.ForeignKey('core.Event', verbose_name=u'Tapahtuma')

    description = models.CharField(
        blank=True,
        max_length=63,
        verbose_name=u'Kuvaus'
    )

    start_time = models.DateTimeField(verbose_name=u'Alkuaika')
    end_time = models.DateTimeField(verbose_name=u'Loppuaika')

    class Meta:
        verbose_name = u'työvuorotoive'
        verbose_name_plural=u'työvuorotoiveet'

    def __unicode__(self):
        datetime_format = '%a %H:%M:%S'
        return u'{description} ({start_time} - {end_time})'.format(
            description=self.description,
            start_time=self.start_time.strftime(datetime_format),
            end_time=self.end_time.strftime(datetime_format),
        )


ONE_HOUR = timedelta(hours=1)


class Job(models.Model):
    job_category = models.ForeignKey(JobCategory, verbose_name=u'tehtäväalue')
    title = models.CharField(max_length=63, verbose_name=u'tehtävän nimi')

    class Meta:
        verbose_name = u'tehtävä'
        verbose_name_plural = u'tehtävät'

    def __unicode__(self):
        return self.title

    @property
    def expanded_requirements(self):
        requirements = []

        for hour in self.job_category.event.labour_event_meta.work_hours:
            try:
                job_requirement = self.jobrequirement_set.get(
                    start_time__lte=hour,
                    end_time__gt=hour,
                )
                count = job_requirement.count
            except JobRequirement.DoesNotExist:
                count = 0

            requirements.append(JobRequirement(
                job=self,
                start_time=hour,
                end_time=hour + ONE_HOUR,
                count=count
            ))

        return requirements


class JobRequirement(models.Model):
    job = models.ForeignKey(Job, verbose_name=u'tehtävä')

    count = models.IntegerField(
        verbose_name=u'vaadittu henkilömäärä',
        validators=[MinValueValidator(0)],
        default=0
    )

    start_time = models.DateTimeField(verbose_name=u'vaatimuksen alkuaika')
    end_time = models.DateTimeField(verbose_name=u'vaatimuksen päättymisaika')

    class Meta:
        verbose_name = u'henkilöstövaatimus'
        verbose_name_plural = u'henkilöstövaatimukset'


NUM_FIRST_CATEGORIES = 5


class Signup(models.Model):
    person = models.ForeignKey('core.Person')
    event = models.ForeignKey('core.Event')

    job_categories = models.ManyToManyField(JobCategory,
        verbose_name=u'Haettavat tehtävät',
        help_text=u'Valitse kaikki ne tehtävät, joissa olisit valmis työskentelemään '
            u'tapahtumassa.',
        related_name='signup_set'
    )

    work_periods = models.ManyToManyField(WorkPeriod,
        verbose_name=u'Työvuorotoiveet',
        help_text=u'Valitse kaikki ne ajanjaksot, joina voit työskennellä tapahtumassa. '
            u'Tämä ei ole lopullinen työvuorosi, vaan työvoimatiimi pyrkii sijoittamaan '
            u'työvuorosi näille ajoille.',
        related_name='signup_set'
    )

    notes = models.TextField(
        blank=True,
        verbose_name=u'Käsittelijän merkinnät',
        help_text=u'Tämä kenttä ei normaalisti näy henkilölle itselleen, mutta jos tämä '
            u'pyytää henkilörekisteriotetta, kentän arvo on siihen sisällytettävä.'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Luotu')
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u'Päivitetty')

    job_accepted = models.ForeignKey(JobCategory,
        blank=True,
        null=True,
        related_name='accepted_signup_set'
    )

    is_rejected = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'ilmoittautuminen'
        verbose_name_plural=u'ilmoittautumiset'

    def __unicode__(self):
        p = self.person.full_name if self.person else 'None'
        e = self.event.name if self.event else 'None'

        return '{p} / {e}'.format(**locals())

    def clean(self):
        if self.is_rejected and self.job_accepted:
            from django.core.exceptions import ValidationError
            raise ValidationError(u'Hakija ei voi olla yhtä aikaa hyväksytty ja hylätty.')

    @property
    def signup_extra(self):
        SignupExtra = self.event.labour_event_meta.signup_extra_model

        try:
            return SignupExtra.objects.get(signup=self)
        except SignupExtra.DoesNotExist:
            return SignupExtra(signup=self)

    def get_first_categories(self):
        return self.job_categories.all()[:NUM_FIRST_CATEGORIES]

    @property
    def is_more_categories(self):
        return self.job_categories.count() > NUM_FIRST_CATEGORIES

    def get_redacted_category_names(self):
        return u', '.join(cat.name for cat in self.job_categories.all()[NUM_FIRST_CATEGORIES:])

    @property
    def is_shifts_complete(self):
        # TODO
        return False


class SignupExtraBase(models.Model):
    signup = models.OneToOneField(Signup, related_name="+", primary_key=True)

    def __unicode__(self):
        return self.signup.__unicode__() if self.signup else 'None'

    @classmethod
    def get_form_class(cls):
        raise NotImplemented('Remember to implement form_class in your SignupExtra class')

    class Meta:
        abstract = True


class EmptySignupExtra(SignupExtraBase):
    @classmethod
    def get_form_class(cls):
        from .forms import EmptySignupExtraForm
        return EmptySignupExtraForm


class Message(models.Model):
    event = models.ForeignKey('core.Event')
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


__all__ = [
    'LabourEventMeta',
    'Job',
    'JobCategory',
    'PersonQualification',
    'Qualification',
    'QualificationExtraBase',
    'Signup',
    'SignupExtraBase',
]
