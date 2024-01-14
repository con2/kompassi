from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TicketsAppConfig(AppConfig):
    name = "tickets"
    verbose_name = _("Ticket sales")

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
