import logging

from celery import shared_task

from .utils import _import_programme


logger = logging.getLogger("kompassi")


@shared_task(ignore_result=True)
def import_programme(event_id, payload):
    from core.models import Event

    event = Event.objects.get(id=event_id)
    _import_programme(event, payload)
