# encoding: utf-8



from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EnrollmentConfig(AppConfig):
    name = 'enrollment'
    verbose_name = _('Enrollment')
