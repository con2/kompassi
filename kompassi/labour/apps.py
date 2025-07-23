from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LabourAppConfig(AppConfig):
    name = "kompassi.labour"
    verbose_name = _("Volunteer management")

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
