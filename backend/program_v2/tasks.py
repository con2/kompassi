import logging

from celery import shared_task

from .models.event_annotation import EventAnnotation

logger = logging.getLogger("kompassi")


@shared_task(ignore_result=True)
def event_annotation_refresh_values(event_id: int, annotation_slug: str):
    event_annotation = EventAnnotation.objects.get(
        meta__event_id=event_id,
        annotation__slug=annotation_slug,
    )
    event_annotation.refresh_values()
