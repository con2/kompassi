from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProgramV2AppConfig(AppConfig):
    name = "kompassi.program_v2"
    verbose_name = _("Program management (v2)")

    def ready(self) -> None:
        from . import event_log_entry_types  # noqa: F401
