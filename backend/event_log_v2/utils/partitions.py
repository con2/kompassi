import logging
from datetime import date
from typing import Any

from django.db import connection, transaction

from ..utils.uuid7 import uuid7_range_for_month

logger = logging.getLogger("kompassi")


class PartitionsMixin:
    _meta: Any

    @classmethod
    def get_current_partition_names(cls) -> set[str]:
        """
        Returns the names of the monthly partitions that currently exist for this model.
        """
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select
                    table_name
                from
                    information_schema.tables
                where
                    table_schema = 'public'
                    and table_name like %s
                """,
                [f"{cls._meta.db_table}_y%"],
            )

            return {row[0] for row in cursor.fetchall()}

    @classmethod
    def get_partition_name(cls, year: int, month: int) -> str:
        return f"{cls._meta.db_table}_y{year}m{month:02d}"

    @classmethod
    def get_expected_partitions(
        cls,
        months_past=6,
        months_future=2,
        today: date | None = None,
    ) -> list[tuple[int, int]]:
        """
        Returns the monthly partitions expected to exist in the current month.
        Used by the list filter in admin and the management command to create missing partitions.

        >>> Entry.get_current_partitions(months_past=2, months_future=1, today=date(2023,1,27))
        [(2022, 11), (2022, 12), (2023, 1), (2023, 2)]
        """
        if today is None:
            today = date.today()
        year, month = today.year, today.month

        expected_partitions = []
        for i in range(-months_past, months_future + 1):
            year_offset, month_offset = divmod(month + i - 1, 12)
            part_year = year + year_offset
            part_month = month_offset + 1

            expected_partitions.append((part_year, part_month))

        return expected_partitions

    @classmethod
    def ensure_partitions(
        cls,
        months_past=6,
        months_future=2,
        today: date | None = None,
    ):
        """
        Ensures that monthly partitions exist for this model in the current month.
        Used by the management command to create missing partitions.
        """
        from ..utils.emit import emit

        if today is None:
            today = date.today()

        expected_partitions = cls.get_expected_partitions(months_past, months_future, today)
        expected_partition_names = {cls.get_partition_name(year, month) for year, month in expected_partitions}
        current_partition_names = cls.get_current_partition_names()
        expired_partition_names = current_partition_names - expected_partition_names
        missing_partitions = [
            (name, year, month)
            for (year, month) in expected_partitions
            if (name := cls.get_partition_name(year, month)) not in current_partition_names
        ]
        table_name = cls._meta.db_table

        if expired_partition_names:
            logger.info("Expired partitions: %s", ", ".join(expired_partition_names))
        if missing_partitions:
            logger.info("Missing partitions: %s", ", ".join(name for (name, _, _) in missing_partitions))

        # move today's partition first in missing_partitions so that emit() won't fail
        todays_partition_index = next(
            (
                i
                for i, (name, year, month) in enumerate(missing_partitions)
                if year == today.year and month == today.month
            ),
            None,
        )
        if todays_partition_index is not None:
            missing_partitions.insert(0, missing_partitions.pop(todays_partition_index))

        with connection.cursor() as cursor:
            for partition_name, year, month in missing_partitions:
                logger.info("Creating partition %s", partition_name)
                with transaction.atomic():
                    start, end = uuid7_range_for_month(year, month)
                    cursor.execute(
                        f"create table {partition_name} partition of {table_name} for values from (%s) to (%s)",
                        [start, end],
                    )
                    emit(
                        f"{cls._meta.app_label}.{cls._meta.model_name}.partition_created",
                        partition_name=partition_name,
                    )

            for partition_name in expired_partition_names:
                logger.info("Dropping partition %s", partition_name)
                with transaction.atomic():
                    cursor.execute(f"drop table {partition_name}")
                    emit(
                        f"{cls._meta.app_label}.{cls._meta.model_name}.partition_deleted",
                        partition_name=partition_name,
                    )
