import logging

from django.core.management.base import BaseCommand

from ...models.entry import Entry

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(*args, **opts):
        Entry.ensure_partitions()
