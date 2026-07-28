from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MessagesV2AppConfig(AppConfig):
    name = "kompassi.messages_v2"
    verbose_name = _("Messages (v2)")

    def ready(self) -> None:
        from . import event_log_entry_types  # noqa: F401
