import logging

from django.conf import settings
from django.db import ProgrammingError
from django.core.management import call_command
from django.core.management.base import BaseCommand


logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    args = ""
    help = "Docker development environment entry point"

    def handle(self, *args, **options):
        from core.models import Event

        event = None
        try:
            event = Event.objects.first()
        except ProgrammingError:
            pass

        if event is None:
            call_command("setup")

        call_command("runserver", "0.0.0.0:8000")
