import logging
from datetime import UTC, datetime, timedelta
from datetime import date as date_type
from datetime import time as time_type
from functools import cached_property
from typing import Any, Protocol, TypeVar
from uuid import UUID

from django.contrib import admin
from django.db import connection, models, transaction

from kompassi.tickets_v2.optimized_server.utils.uuid7 import (
    uuid7,
    uuid7_day_range,
    uuid7_month_range,
    uuid7_month_range_for_year_month,
    uuid7_to_datetime,
)

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=models.Model)


class IMeta(Protocol):
    db_table: str
    app_label: str
    model_name: str


class UUID7Mixin:
    """
    Adds useful methods for working with UUID7 primary keys.
    """

    pk: UUID

    @cached_property
    def timestamp(self):
        return uuid7_to_datetime(self.pk)

    @cached_property
    def created_at(self):
        return self.timestamp

    @property
    def date(self):
        return self.timestamp.date()

    @admin.display(description="date", ordering="id")
    def admin_get_date(self):
        return self.date

    @staticmethod
    def year_month_filter(queryset: models.QuerySet[T], year: int, month: int) -> models.QuerySet[T]:
        while month < 1:
            month += 12
            year -= 1
        while month > 12:
            month -= 12
            year += 1

        start, end = uuid7_month_range_for_year_month(year, month)
        return queryset.filter(id__gte=start, id__lt=end)

    @staticmethod
    def year_month_gte_filter(queryset: models.QuerySet[T], year: int, month: int) -> models.QuerySet[T]:
        while month < 1:
            month += 12
            year -= 1
        while month > 12:
            month -= 12
            year += 1

        start = uuid7(datetime(year, month, 1, tzinfo=UTC), rand=0)
        return queryset.filter(id__gte=start)

    @staticmethod
    def year_month_lt_filter(queryset: models.QuerySet[T], year: int, month: int) -> models.QuerySet[T]:
        while month < 1:
            month += 12
            year -= 1
        while month > 12:
            month -= 12
            year += 1

        start = uuid7(datetime(year, month, 1, tzinfo=UTC), rand=0)
        return queryset.filter(id__lt=start)

    @staticmethod
    def year_filter(queryset: models.QuerySet[T], year: int) -> models.QuerySet[T]:
        start = uuid7(datetime(year, 1, 1, tzinfo=UTC), rand=0)
        end = uuid7(datetime(year + 1, 1, 1, tzinfo=UTC), rand=0)
        return queryset.filter(id__gte=start, id__lt=end)

    @classmethod
    def maybe_year_month_filter(
        cls,
        queryset: models.QuerySet[T],
        year: int | None,
        month: int | None,
    ) -> models.QuerySet[T]:
        if month is not None and year is None:
            raise ValueError("Cannot filter by month without year")

        if year is not None:
            if month is not None:
                return cls.year_month_filter(queryset, year, month)
            else:
                return cls.year_filter(queryset, year)

        return queryset

    @staticmethod
    def month_filter(queryset: models.QuerySet[T], d: datetime | date_type) -> models.QuerySet[T]:
        start, end = uuid7_month_range(d)
        return queryset.filter(id__gte=start, id__lt=end)

    @staticmethod
    def date_filter(queryset: models.QuerySet[T], d: datetime | date_type) -> models.QuerySet[T]:
        start, end = uuid7_day_range(d)
        return queryset.filter(id__gte=start, id__lt=end)

    @staticmethod
    def date_filter_with_slack(
        queryset: models.QuerySet[T],
        d: datetime | date_type,
        slack: timedelta,
    ) -> models.QuerySet[T]:
        if isinstance(d, datetime):
            d = d.date()

        start = uuid7(datetime.combine(d - slack, time_type(0), UTC))
        end = uuid7(datetime.combine(d + timedelta(days=1) + slack, time_type(0), UTC))

        return queryset.filter(id__gte=start, id__lt=end)

    def make_colocated_id(self):
        """
        Returns an UUID7 that shares the timestamp with the object's UUID.
        """
        return uuid7(uuid7_to_datetime(self.pk))


class MonthlyPartitionsMixin(UUID7Mixin):
    _meta: Any

    @classmethod
    def get_current_partition_names(cls) -> set[str]:
        """
        Returns the names of the monthly partitions that currently exist for this model.
        """
        meta: IMeta = cls._meta

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
                [f"{meta.db_table}_y%"],
            )

            return {row[0] for row in cursor.fetchall()}

    @classmethod
    def get_partition_name(cls, year: int, month: int) -> str:
        meta: IMeta = cls._meta
        return f"{meta.db_table}_y{year}m{month:02d}"

    @classmethod
    def get_expected_partitions(
        cls,
        months_past=6,
        months_future=2,
        today: date_type | None = None,
    ) -> list[tuple[int, int]]:
        """
        Returns the monthly partitions expected to exist in the current month.
        Used by the list filter in admin and the management command to create missing partitions.

        >>> Entry.get_current_partitions(months_past=2, months_future=1, today=date(2023,1,27))
        [(2022, 11), (2022, 12), (2023, 1), (2023, 2)]
        """
        if today is None:
            today = datetime.now(UTC).date()

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
        today: date_type | None = None,
    ):
        """
        Ensures that monthly partitions exist for this model in the current month.
        Used by the management command to create missing partitions.
        """
        from .emit import emit

        if today is None:
            today = datetime.now(UTC).date()

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
                    start, end = uuid7_month_range_for_year_month(year, month)
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
