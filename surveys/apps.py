# encoding: utf-8

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SurveysAppConfig(AppConfig):
    name = 'surveys'
    verbose_name = _('Surveys')