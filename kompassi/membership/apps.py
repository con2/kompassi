from django.apps import AppConfig


class MembershipAppConfig(AppConfig):
    name = "kompassi.membership"
    verbose_name = "Jäsenrekisteri"

    def ready(self):
        from . import event_log_entry_types  # noqa: F401
