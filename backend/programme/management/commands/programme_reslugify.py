import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Programme

logger = logging.getLogger("kompassi")


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Re-create slugs for programme v1 items"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

        parser.add_argument(
            "--really",
            action="store_true",
            default=False,
        )

    def handle(*args, **opts):
        with transaction.atomic():
            queryset = Programme.objects.filter(category__event__slug__in=opts["event_slugs"])
            Programme.reslugify(queryset)

            if not opts["really"]:
                raise NotReally("It was only a dream :)")
