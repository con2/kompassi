from __future__ import annotations

import logging
from typing import Any, ClassVar

from django.db import connection

from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.monthly_partitions import IMeta

logger = logging.getLogger(__name__)


class EventPartitionsMixin:
    _meta: Any

    intrapartition_id_column: ClassVar[str] = "id"

    @classmethod
    def partition_exists(cls, event: Event) -> bool:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select 1
                from information_schema.tables
                where table_schema = 'public' and table_name = %s
                """,
                [cls.get_partition_name(event)],
            )

            return cursor.fetchone() is not None

    @classmethod
    def create_partition(cls, event: Event):
        meta: IMeta = cls._meta
        partition_name = cls.get_partition_name(event)

        logger.info(f"Creating partition {partition_name}")

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                create table {partition_name}
                partition of {meta.db_table}
                for values in (%s)
                """,
                [event.id],
            )

    @classmethod
    def fix_statistics(cls, event: Event):
        """
        Postgres, when left to its own devices, is prone to do seq scans on
        our ticket tables. This is because it thinks that the id column is
        not selective enough. We know better, and we can fix this by
        increasing the statistics target for the id column.

        Normally this would be overridden by autovacuum, but partitioned
        tables are not autovacuumed with ANALYZE. So the statistics target
        we set here will stick.

        The statistics target represents how many distinct values
        there are in the column. We know that the id column is unique, so
        we can set the statistics target to the maximum value of 10000.
        """
        partition_name = cls.get_partition_name(event)

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                alter table {partition_name}
                alter column {cls.intrapartition_id_column}
                set statistics 10000
                """
            )

    @classmethod
    def ensure_partition(cls, event: Event):
        created = False

        if cls.partition_exists(event):
            logger.debug(f"Partition {cls.get_partition_name(event)} already exists")
        else:
            cls.create_partition(event)
            created = True

        cls.fix_statistics(event)

        return created

    @classmethod
    def get_partition_name(cls, event: Event):
        meta: IMeta = cls._meta
        satanized_slug = event.slug.replace("-", "")
        return f"{meta.db_table}_{satanized_slug}"
