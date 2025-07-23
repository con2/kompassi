from django.apps import AppConfig


class TicketsV2Config(AppConfig):
    name = "kompassi.tickets_v2"
    verbose_name = "Tickets V2"

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
