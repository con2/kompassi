from django.apps import AppConfig


class ProgramV2AppConfig(AppConfig):
    name = "involvement"
    verbose_name = "Involvement"

    def ready(self) -> None:
        from . import handlers  # noqa: F401
