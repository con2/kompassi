from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DirectoryAppConfig(AppConfig):
    name = "directory"
    verbose_name = _("directory")

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
