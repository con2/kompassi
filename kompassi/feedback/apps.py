from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FeedbackAppConfig(AppConfig):
    name = "kompassi.feedback"
    verbose_name = _("feedback")

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
