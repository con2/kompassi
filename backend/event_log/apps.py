from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventLogAppConfig(AppConfig):
    name = "event_log"
    verbose_name = _("event log")

    def ready(self):
        from . import handlers  # noqa: F401
