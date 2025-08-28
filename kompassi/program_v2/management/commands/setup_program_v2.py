from __future__ import annotations

from django.core.management.base import BaseCommand

from kompassi.program_v2.annotations import setup_program_annotations


class Command(BaseCommand):
    help = "Setup program v2"

    def handle(self, *args, **options):
        setup_program_annotations()
