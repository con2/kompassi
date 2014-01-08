from django.db import models
from django.utils.timezone import now


class LabourEventMeta(models.Model):
    event = models.OneToOneField('core.Event', primary_key=True)
    signup_extra_content_type = models.ForeignKey('contenttypes.ContentType')

    registration_opens = models.DateTimeField(null=True, blank=True)
    registration_closes = models.DateTimeField(null=True, blank=True)

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


class Signup(models.Model):
    person = models.ForeignKey('core.Person')
    event = models.ForeignKey('core.Event')

    @property
    def signup_extra(self):
        return self.event.signup_extra_model.objects.get(signup=self)    


class SignupExtraBase(models.Model):
    signup = models.OneToOneField(Signup, related_name="+", primary_key=True)

    @classmethod
    def init_form(cls, *args, **kwargs):
        raise NotImplemented('Remember to override init_form in your SignupExtra model')

    class Meta:
        abstract = True


class Qualification(models.Model):
    name = models.CharField(max_length=31)
    qualification_extra_content_type = models.ForeignKey('contenttypes.ContentType', null=True, blank=True)

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

    @property
    def qualification_extra(self):
        return self.qualification.qualification_extra_model.objects.get(personqualification=self)


class QualificationExtraBase(models.Model):
    personqualification = models.OneToOneField(PersonQualification, related_name="+", primary_key=True)

    @classmethod
    def init_form(cls, *args, **kwargs):
        raise NotImplemented('Remember to override init_form in your QualificationExtra model')

    class Meta:
        abstract = True


__all__ = [
	'EventMeta',
	'PersonQualification',
	'Qualification',
	'QualificationExtraBase'
	'Signup',
	'SignupExtraBase',
]
