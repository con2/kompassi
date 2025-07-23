from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreAppConfig(AppConfig):
    name = "kompassi.core"
    verbose_name = _("core")

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
