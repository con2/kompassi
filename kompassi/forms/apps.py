from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FormsAppConfig(AppConfig):
    name = "kompassi.forms"
    verbose_name = _("Forms")

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
