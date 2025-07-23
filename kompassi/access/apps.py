from django.apps import AppConfig


class AccessAppConfig(AppConfig):
    name = "kompassi.access"
    verbose_name = "Pääsynhallinta"

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
