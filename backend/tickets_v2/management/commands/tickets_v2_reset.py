import logging

from django.core.management.base import BaseCommand
from django.db import connection, transaction

logger = logging.getLogger("kompassi")


class NotReally(Exception):
    pass


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Check that all orders are assigned the correct amount of tickets"

    def add_arguments(self, parser):
        parser.add_argument("--really", default=False, action="store_true")

    def handle(*args, **opts):
        with transaction.atomic(), connection.cursor() as cursor:
            cursor.execute(
                """
                    truncate
                        tickets_v2_ticket,
                        tickets_v2_order,
                        tickets_v2_quota,
                        tickets_v2_product,
                        tickets_v2_paymentstamp,
                        tickets_v2_receipt,
                        tickets_v2_ticketsv2eventmeta
                    restart identity
                    cascade
                """
            )

            if not opts["really"]:
                raise NotReally(
                    "Use --really to actually reset the database. You probably shouldn't do this in production :))"
                )

            logger.info("Resetting all tickets_v2 tables.")
