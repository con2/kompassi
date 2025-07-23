import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class NotReally(Exception):
    pass


class Command(BaseCommand):
    help = "Configure the tickets_v2 app for performance testing"

    def add_arguments(self, parser):
        parser.add_argument("--really", default=False, action="store_true")

    def handle(*args, **opts):
        if not opts["really"]:
            raise NotReally(
                "Use --really to actually reset the database. You probably shouldn't do this in production :))"
            )

        # overkill
        # call_command("migrate", "tickets_v2", "zero")
        # call_command("migrate")

        call_command("tickets_v2_reset", really=True)
        call_command("setup_tracon2025", dev_tickets=True)
