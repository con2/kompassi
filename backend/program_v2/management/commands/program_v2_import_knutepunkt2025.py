import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from ...importers.knutepunkt2025 import import_knutepunkt

logger = logging.getLogger("kompassi")


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Import Knutepunkt 2025 into Program V2 (eg. production)"

    def handle(*args, **opts):
        with transaction.atomic():
            import_knutepunkt("knutepunkt2025")
