from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProgrammeAppConfig(AppConfig):
    name = "programme"
    verbose_name = _("programme management")

    def ready(self):
        from . import handlers  # noqa
