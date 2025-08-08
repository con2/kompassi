from __future__ import annotations

from django.core.management.base import BaseCommand

from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.program_v2.annotations import PROGRAM_ANNOTATIONS


class Command(BaseCommand):
    help = "Setup program v2"

    def handle(self, *args, **options):
        AnnotationDTO.save_many(PROGRAM_ANNOTATIONS)
