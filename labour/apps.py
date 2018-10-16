from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LabourAppConfig(AppConfig):
    name = 'labour'
    verbose_name = _('Volunteer management')

    def ready(self):
        from . import event_log_entry_types  # noqa
