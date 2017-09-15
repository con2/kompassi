from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoreAppConfig(AppConfig):
    name = 'core'
    verbose_name = _('core')

    def ready(self):
        from . import event_log_entry_types  # noqa
