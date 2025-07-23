import logging

from django.db import transaction

from kompassi.celery_app import app
from kompassi.program_v2.models.program import Program
from kompassi.program_v2.utils.extract_annotations import extract_annotations_from_responses

from .models.event_annotation import EventAnnotation

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def event_annotation_refresh_values(event_id: int, annotation_id: int):
    for program_id in Program.objects.filter(event_id=event_id).order_by("id").values_list("id", flat=True):
        event_annotation_refresh_values_program.delay(event_id, annotation_id, program_id)  # type: ignore


@app.task(ignore_result=True)
def event_annotation_refresh_values_program(event_id: int, annotation_id: int, program_id: int):
    with transaction.atomic():
        program = Program.objects.select_for_update(of=("self",), no_key=True).get(id=program_id)
        event_annotation = EventAnnotation.objects.get(meta_id=event_id, annotation_id=annotation_id)
        program.refresh_annotations(
            extract_annotations_from_responses(
                responses=program.responses.all(),
                event_annotations=[event_annotation],
            )
        )
        program.refresh_dependents()
