from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventLogAppConfig(AppConfig):
    name = "kompassi.event_log_v2"
    verbose_name = _("event log v2")

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
