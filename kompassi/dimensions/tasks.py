import logging

from django.db import transaction

from kompassi.celery_app import app

from .models.enums import DimensionApp
from .models.universe import Universe
from .models.universe_annotation import UniverseAnnotation

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def universe_annotation_refresh_values(universe_id: int, annotation_id: int):
    from kompassi.program_v2.models.program import Program

    universe = Universe.objects.get(id=universe_id)
    match universe.app:
        case DimensionApp.PROGRAM_V2:
            event = universe.scope.event
            if event is None:
                raise ValueError("cannot be!")
            for program_id in Program.objects.filter(event=event).order_by("id").values_list("id", flat=True):
                universe_annotation_refresh_values_program.delay(universe_id, annotation_id, program_id)  # type: ignore


@app.task(ignore_result=True)
def universe_annotation_refresh_values_program(universe_id: int, annotation_id: int, program_id: int):
    from kompassi.forms.utils.extract_annotations import extract_annotations_from_responses
    from kompassi.program_v2.models.program import Program

    with transaction.atomic():
        program = Program.objects.select_for_update(of=("self",), no_key=True).get(id=program_id)
        universe_annotation = UniverseAnnotation.objects.get(universe_id=universe_id, annotation_id=annotation_id)
        program.refresh_annotations(
            extract_annotations_from_responses(
                responses=program.responses.all(),
                universe_annotations=[universe_annotation],
            )
        )
        program.refresh_dependents()
