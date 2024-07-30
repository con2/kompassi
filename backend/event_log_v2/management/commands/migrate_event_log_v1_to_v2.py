import logging
from datetime import UTC, datetime
from itertools import batched

from django.core.management.base import BaseCommand
from django.db import connection, transaction

from zombies.event_log.models.entry import Entry as ObsoleteEntry

from ...models.entry import Entry
from ...utils.uuid7 import uuid7

logger = logging.getLogger("kompassi")
batch_size = 400


class Command(BaseCommand):
    """
    Migrate event log entries from event log V1 to V2.

    NOTE: Events older than the retention window (6 previous full calendar months) will be discarded.
    """

    def handle(*args, **opts):
        partitions = Entry.get_expected_partitions()
        for year, month in partitions:
            december = 12
            start = datetime(year, month, 1, tzinfo=UTC)
            end = start.replace(month=month + 1) if month < december else start.replace(year=year + 1, month=1)

            with transaction.atomic():
                entries = (
                    ObsoleteEntry.objects.filter(
                        created_at__gte=start,
                        created_at__lt=end,
                    )
                    .order_by("created_at")
                    .select_for_update()
                )
                for page, page_entries in enumerate(
                    batched(entries, batch_size),
                    start=1,
                ):
                    logger.info("Migrating %s, page %d", Entry.get_partition_name(year, month), page)
                    bulk_create = []
                    for entry in page_entries:
                        id = uuid7(entry.created_at)

                        other_fields = dict(entry.other_fields)
                        if entry.event:
                            other_fields["event"] = entry.event.slug
                            other_fields["organization"] = entry.event.organization.slug
                        elif entry.organization:
                            other_fields["organization"] = entry.organization.slug

                        for other_field_name in ("ip_address", "context", "search_term"):
                            # as-is fields
                            if (value := getattr(entry, other_field_name)) not in (None, ""):
                                other_fields[other_field_name] = value

                        for other_field_name in (
                            "person",
                            "accommodation_information",
                            "limit_group",
                        ):
                            # fkey fields
                            if (value := getattr(entry, other_field_name)) is not None:
                                other_fields[other_field_name] = value.pk

                        bulk_create.append(
                            Entry(
                                id=id,
                                actor=entry.created_by,
                                entry_type=entry.entry_type,
                                other_fields=other_fields,
                            )
                        )
                    Entry.objects.bulk_create(bulk_create)

        # empty obsolete table efficiently
        with connection.cursor() as cursor:
            logger.info("Emptying obsolete table %s", ObsoleteEntry._meta.db_table)
            cursor.execute(f"truncate table {ObsoleteEntry._meta.db_table}")
