# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class SignupExtraBase(models.Model):
    signup = models.OneToOneField('labour.Signup', related_name="%(app_label)s_signup_extra", primary_key=True)

    def __unicode__(self):
        return self.signup.__unicode__() if self.signup else 'None'

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

    class Meta:
        abstract = True


class EmptySignupExtra(SignupExtraBase):
    @classmethod
    def get_form_class(cls):
        from ..forms import EmptySignupExtraForm
        return EmptySignupExtraForm