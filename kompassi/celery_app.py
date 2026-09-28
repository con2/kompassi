import logging.config
import os

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kompassi.settings")

app = Celery("kompassi")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@setup_logging.connect
def configure_logging_from_django_settings(**kwargs):
    logging.config.dictConfig(settings.LOGGING)
