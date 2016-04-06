# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class SignupExtraMixin(object):
    @classmethod
    def get_form_class(cls):
        raise NotImplemented('Remember to implement form_class in your SignupExtra class')

    @staticmethod
    def get_query_class():
        return None

    @classmethod
    def get_shirt_size_field(cls):
        if not hasattr(cls, '_shirt_size_field'):
            cls._shirt_size_field = None
            for field in cls._meta.fields:
                if field.name == 'shirt_size':
                    cls._shirt_size_field = field
                    break

        return cls._shirt_size_field

    @classmethod
    def get_shirt_type_field(cls):
        if not hasattr(cls, '_shirt_type_field'):
            cls._shirt_type_field = None
            for field in cls._meta.fields:
                if field.name == 'shirt_type':
                    cls._shirt_type_field = field
                    break

        return cls._shirt_type_field

    @classmethod
    def get_field(cls, field_name):
        if not hasattr(cls, '_fields_by_name'):
            cls._fields_by_name = dict((field.name, field) for field in cls._meta.fields)

        return cls._fields_by_name.get(field_name)

    def __unicode__(self):
        return self.signup.__unicode__() if self.signup else 'None'


class SignupExtraBase(SignupExtraMixin, models.Model):
    event = models.ForeignKey('core.Event', related_name="%(app_label)s_signup_extras")
    person = models.OneToOneField('core.Event', related_name="%(app_label)s_signup_extra")

    @classmethod
    def get_for_event_and_person(cls, event, person):
        return cls.objects.get(event=event, person=person)

    class Meta:
        abstract = True


class ObsoleteSignupExtraBaseV1(models.Model):
    """
    Because `signup` is the primary key, we choose to retain this abstract base model and make a new one
    that refers to `event` and `person` instead.
    """
    signup = models.OneToOneField('labour.Signup', related_name="%(app_label)s_signup_extra", primary_key=True)

    @property
    def event(self):
        return self.signup.event if self.signup is not None else None

    @property
    def person(self):
        return self.signup.person if self.person is not None else None

    @classmethod
    def get_for_event_and_person(cls, event, person):
        return cls.objects.get(signup__event=event, signup__person=person)

    class Meta:
        abstract = True


class ObsoleteEmptySignupExtraV1(ObsoleteSignupExtraBaseV1):
    @classmethod
    def get_form_class(cls):
        from ..forms import ObsoleteEmptySignupExtraV1Form
        return ObsoleteEmptySignupExtraV1Form
