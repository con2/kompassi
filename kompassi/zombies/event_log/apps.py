from django.apps import AppConfig


class EventLogAppConfig(AppConfig):
    """
    Superseded by event_log_v2.
    """

    name = "kompassi.zombies.event_log"
    verbose_name = "Event log V1 (Obsolete)"
