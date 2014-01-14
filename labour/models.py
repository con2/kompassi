# encoding: utf-8

from datetime import date, datetime, timedelta

from django.db import models
from django.utils.timezone import now

from core.utils import SlugField


class LabourEventMeta(models.Model):
    event = models.OneToOneField('core.Event', primary_key=True)
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

    admin_group = models.ForeignKey('auth.Group')

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
    def create_dummy(cls):
        from core.models import Event
        from django.contrib.auth.models import Group
        from django.contrib.contenttypes.models import ContentType

        event = Event.create_dummy()
        group = Group.objects.create(name='Dummy group')
        content_type = ContentType.objects.get_for_model(EmptySignupExtra)

        t = now()

        return cls.objects.create(
            event=event,
            admin_group=group,
            signup_extra_content_type=content_type,
            registration_opens=t - timedelta(days=60),
            registration_closes=t + timedelta(days=60)
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


class Qualification(models.Model):
    slug = SlugField()

    name = models.CharField(max_length=31, verbose_name=u'pätevyyden nimi')
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

    name = models.CharField(max_length=31, verbose_name=u'tehtäväalueen nimi')

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


NUM_FIRST_CATEGORIES = 5


class Signup(models.Model):
    person = models.ForeignKey('core.Person')
    event = models.ForeignKey('core.Event')

    job_categories = models.ManyToManyField(JobCategory,
        verbose_name=u'Haettavat tehtävät',
        help_text=u'TODO kuvaukset tulee näkyviin kun kerkiää. Valitse kaikki ne tehtävät, '
            u'joissa olisit valmis työskentelemään tapahtumassa.',
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
        SignupExtra = self.event.laboureventmeta.signup_extra_model

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


__all__ = [
    'LabourEventMeta',
    'JobCategory',
    'PersonQualification',
    'Qualification',
    'QualificationExtraBase',
    'Signup',
    'SignupExtraBase',
]
