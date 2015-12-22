from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LabourAppConfig(AppConfig):
    name = 'labour'
    verbose_name = _(u'Volunteer management')