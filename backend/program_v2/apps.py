from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProgramV2AppConfig(AppConfig):
    name = "program_v2"
    verbose_name = _("Program management (v2)")

    def ready(self) -> None:
        from . import handlers  # noqa: F401
