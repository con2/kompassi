from django.apps import AppConfig


class ProgramV2AppConfig(AppConfig):
    name = "kompassi.involvement"
    verbose_name = "Involvement"

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
