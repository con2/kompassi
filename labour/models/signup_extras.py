# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class SignupExtraMixin(object):
    @classmethod
    def get_form_class(cls):
        raise NotImplementedError('Remember to implement form_class in your SignupExtra class')

    @classmethod
    def get_programme_form_class(cls):
        return cls.get_form_class()

    @staticmethod
    def get_query_class():
        raise NotImplementedError('Query builder not implemented for this event')

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

    def apply_state(self):
        self.is_active = self.determine_is_active()
        self.save()

    def __unicode__(self):
        return self.signup.__unicode__() if self.signup else 'None'


class SignupExtraBase(SignupExtraMixin, models.Model):
    event = models.ForeignKey('core.Event', related_name="%(app_label)s_signup_extras")
    person = models.OneToOneField('core.Person', related_name="%(app_label)s_signup_extra")

    is_active = models.BooleanField(default=True)

    supports_programme = True

    def determine_is_active(self):
        # See if this SignupExtra is active due to participation in volunteer work
        if self.signup is not None and self.signup.is_active:
            return True

        # See if this SignupExtra is active due to programme roles
        from programme.models.programmerole import ProgrammeRole
        from programme.models.programme import PROGRAMME_STATES_ACTIVE
        return ProgrammeRole.objects.filter(
            programme__category__event=self.event,
            programme__state__in=PROGRAMME_STATES_ACTIVE,
            person=self.person,
        ).exists()

    @property
    def signup(self):
        if not hasattr(self, '_signup'):
            try:
                self._signup = Signup.objects.get(event=self.event, person=self.person)
            except Signup.DoesNotExist:
                self._signup = None

        return self._signup

    @classmethod
    def get_for_event_and_person(cls, event, person):
        return cls.objects.get(event=event, person=person)

    @classmethod
    def for_event_and_person(cls, event, person):
        try:
            return cls.objects.get(event=event, person=person)
        except cls.DoesNotExist:
            return cls(event=event, person=person)

    @classmethod
    def for_signup(cls, signup):
        try:
            return cls.get_for_event_and_person(signup.event, signup.person)
        except cls.DoesNotExist:
            return cls(event=signup.event, person=signup.person)

    class Meta:
        abstract = True


class EmptySignupExtra(SignupExtraBase):
    @classmethod
    def get_form_class(cls):
        from ..forms import EmptySignupExtraForm
        return EmptySignupExtraForm


class ObsoleteSignupExtraBaseV1(SignupExtraMixin, models.Model):
    """
    Because `signup` is the primary key, we choose to retain this abstract base model and make a new one
    that refers to `event` and `person` instead.
    """
    signup = models.OneToOneField('labour.Signup', related_name="%(app_label)s_signup_extra", primary_key=True)
    is_active = models.BooleanField(default=True)

    supports_programme = False

    def determine_is_active(self):
        return self.signup.is_active

    @property
    def event(self):
        return self.signup.event if self.signup is not None else None

    @property
    def person(self):
        return self.signup.person if self.signup is not None else None

    @classmethod
    def get_for_event_and_person(cls, event, person):
        return cls.objects.get(signup__event=event, signup__person=person)

    @classmethod
    def for_signup(cls, signup):
        try:
            return cls.objects.get(signup=signup)
        except cls.DoesNotExist:
            return cls(signup=signup)

    class Meta:
        abstract = True


class ObsoleteEmptySignupExtraV1(ObsoleteSignupExtraBaseV1):
    @classmethod
    def get_form_class(cls):
        from ..forms import ObsoleteEmptySignupExtraV1Form
        return ObsoleteEmptySignupExtraV1Form
