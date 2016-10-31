from django.apps import AppConfig


class KompaqAppConfig(AppConfig):
    name = 'kompaq'
    verbose_name = 'Kompaq AMQP Notifications'

    def ready(self):
        from . import handlers
