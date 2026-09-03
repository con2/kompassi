from __future__ import annotations

from datetime import timedelta


def days_to_timedelta(days: int | None) -> timedelta | None:
    if days is None:
        return None
    return timedelta(days=days)


def timedelta_to_days(period: timedelta | None) -> int | None:
    if period is None:
        return None
    return period.days
