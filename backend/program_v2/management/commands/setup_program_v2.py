from __future__ import annotations

from django.core.management.base import BaseCommand

from program_v2.models.annotation import Annotation


class Command(BaseCommand):
    help = "Setup program v2"

    def handle(self, *args, **options):
        Annotation.ensure()
