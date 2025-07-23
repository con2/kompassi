from django.apps import AppConfig


class TicketsAppConfig(AppConfig):
    name = "kompassi.zombies.tickets"
    verbose_name = "Tickets V1 (Obsolete)"

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
