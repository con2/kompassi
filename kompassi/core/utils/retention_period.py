from __future__ import annotations

from datetime import datetime, timedelta

from django.db.models import DateTimeField, ExpressionWrapper, Func
from django.db.models.functions import TruncYear
from django.utils.timezone import get_default_timezone


def days_to_timedelta(days: int | None) -> timedelta | None:
    if days is None:
        return None
    return timedelta(days=days)


def timedelta_to_days(period: timedelta | None) -> int | None:
    if period is None:
        return None
    return period.days


def retention_reference_time(anchor: datetime) -> datetime:
    """
    The moment a retention period starts counting from: the turn of the year after `anchor`.
    Different years of the same event tend to fall on roughly the same dates, so counting from
    the end of the year rather than from the exact date makes their purges land consistently.
    """
    tz = get_default_timezone()
    return datetime(anchor.astimezone(tz).year + 1, 1, 1, tzinfo=tz)


class RetentionReferenceTime(Func):
    """
    Database counterpart of retention_reference_time. NULL if the anchor is NULL.
    """

    # Postgres does the calendar arithmetic of a month-based interval in the session time zone,
    # which Django keeps at UTC. That is safe here because New Year is never inside daylight
    # saving time, so the UTC offset is the same on both sides of the addition.
    template = "(%(expressions)s + interval '1 year')"
    arity = 1
    output_field = DateTimeField()

    def __init__(self, anchor):
        super().__init__(TruncYear(anchor, tzinfo=get_default_timezone()))


def retain_until(anchor, retention_period) -> ExpressionWrapper:
    """
    Annotation for the moment `retention_period` (a DurationField expression) has passed since
    the retention reference time of `anchor` (a DateTimeField expression). NULL if either is
    NULL, which never compares as expired and thus retains the row indefinitely.
    """
    return ExpressionWrapper(RetentionReferenceTime(anchor) + retention_period, output_field=DateTimeField())
