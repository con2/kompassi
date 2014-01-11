# encoding: utf-8

from django.db import models
from django.utils.timezone import now


class LabourEventMeta(models.Model):
    event = models.OneToOneField('core.Event', primary_key=True)
    signup_extra_content_type = models.ForeignKey('contenttypes.ContentType')

    registration_opens = models.DateTimeField(null=True, blank=True)
    registration_closes = models.DateTimeField(null=True, blank=True)

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


class Qualification(models.Model):
    slug = models.CharField(max_length=31, primary_key=True)
    name = models.CharField(max_length=31)
    description = models.TextField()
    qualification_extra_content_type = models.ForeignKey('contenttypes.ContentType', null=True, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def qualification_extra_model(self):
        return self.qualification_extra_content_type.model_class() if self.qualification_extra_content_type else None

    @classmethod
    def create_dummy(cls):
        return cls.objects.create(
            name='Dummy qualification'
        )


class PersonQualification(models.Model):
    person = models.ForeignKey('core.Person')
    qualification = models.ForeignKey(Qualification)

    def __unicode__(self):
        p = self.person.full_name if self.person else 'None'
        q = self.qualification.name if self.qualification else 'None'

        return "{p} / {q}".format(**locals())

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
    personqualification = models.OneToOneField(PersonQualification, related_name="+", primary_key=True)

    @classmethod
    def get_form_class(cls):
        raise NotImplemented('Remember to override get_form_class in your QualificationExtra model')

    class Meta:
        abstract = True


class JobCategory(models.Model):
    event = models.ForeignKey('core.Event')

    name = models.CharField(max_length=31)
    description = models.TextField()
    public = models.BooleanField(default=True)

    required_qualifications = models.ManyToManyField(Qualification, blank=True)

    def __unicode__(self):
        return self.name


class Signup(models.Model):
    person = models.ForeignKey('core.Person')
    event = models.ForeignKey('core.Event')

    job_categories = models.ManyToManyField(JobCategory, verbose_name=u'Haettavat tehtävät', help_text=u'TODO kuvaukset tulee näkyviin kun kerkiää. Valitse kaikki ne tehtävät, joissa olisit valmis työskentelemään tapahtumassa.')

    allergies = models.TextField(blank=True, verbose_name=u'Ruoka-aineallergiat', help_text=u'Tapahtuman järjestäjä pyrkii ottamaan allergiat huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.')
    prior_experience = models.TextField(blank=True, verbose_name=u'Työkokemus', help_text=u'Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä hakemassasi tehtävässä.')
    free_text = models.TextField(blank=True, verbose_name=u'Vapaa alue')

    notes = models.TextField(blank=True, verbose_name=u'Käsittelijän merkinnät', help_text=u'Tämä kenttä ei normaalisti näy henkilölle itselleen, mutta jos tämä pyytää henkilörekisteriotetta, kentän arvo on siihen sisällytettävä.')

    def __unicode__(self):
        p = self.person.full_name if self.person else 'None'
        e = self.event.name if self.event else 'None'

        return '{p} / {e}'.format(**locals())

    @property
    def signup_extra(self):
        SignupExtra = self.event.laboureventmeta.signup_extra_model

        try:
            return SignupExtra.objects.get(signup=self)
        except SignupExtra.DoesNotExist:
            return SignupExtra(signup=self)


class SignupExtraBase(models.Model):
    signup = models.OneToOneField(Signup, related_name="+", primary_key=True)

    def __unicode__(self):
        return self.signup.__unicode__() if self.signup else 'None'        

    @classmethod
    def get_form_class(cls):
        raise NotImplemented('Remember to implement form_class in your SignupExtra class')

    class Meta:
        abstract = True


__all__ = [
    'LabourEventMeta',
    'JobCategory',
    'PersonQualification',
    'Qualification',
    'QualificationExtraBase',
    'Signup',
    'SignupExtraBase',
]
