from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SurveysAppConfig(AppConfig):
    name = "surveys"
    verbose_name = _("Surveys")

    def ready(self):
        from . import event_log_entry_types  # noqa
