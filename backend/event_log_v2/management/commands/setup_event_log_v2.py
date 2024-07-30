import logging

from django.core.management.base import BaseCommand

from ...models.entry import Entry

logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    def handle(*args, **opts):
        Entry.ensure_partitions()
