from django.apps import AppConfig


class ProgrammeAppConfig(AppConfig):
    name = "kompassi.zombies.programme"
    verbose_name = "Programme V1 (Obsolete)"

    def ready(self):
        from . import handlers  # noqa: F401
