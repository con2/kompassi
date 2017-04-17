# encoding: utf-8



from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SurveysAppConfig(AppConfig):
    name = 'surveys'
    verbose_name = _('Surveys')

    def ready(self):
        from . import event_log_entry_types  # noqa
        from . import handlers  # noqa
