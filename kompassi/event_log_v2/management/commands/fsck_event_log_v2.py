import logging
from itertools import batched

from django.core.management.base import BaseCommand
from django.db import transaction

from ...models.entry import Entry

logger = logging.getLogger(__name__)
batch_size = 400


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    """
    Clean up event log entries.
    """

    def add_arguments(self, parser):
        parser.add_argument("--really", default=False, action="store_true")

    def handle(*args, **opts):
        really: bool = opts["really"]

        for year, month in Entry.get_expected_partitions():
            try:
                with transaction.atomic():
                    for page, entries in enumerate(
                        batched(
                            Entry.year_month_filter(Entry.objects.all(), year, month),
                            batch_size,
                        )
                    ):
                        logger.info(f"Processing page {page} of event log entries for {year}-{month}")

                        bulk_update = []
                        for entry in entries:
                            # Remove empty strings and null values
                            new_other_fields = {k: v for (k, v) in entry.other_fields.items() if v not in (None, "")}
                            if new_other_fields != entry.other_fields:
                                entry.other_fields = new_other_fields
                                bulk_update.append(entry)
                        if bulk_update:
                            Entry.objects.bulk_update(bulk_update, ["other_fields"])

                    if not really:
                        raise NotReally("It was only a dream :')")
            except NotReally:
                logger.warning("Dry run, pass --really to actually clean up")
