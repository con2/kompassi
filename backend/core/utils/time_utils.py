import sys
from datetime import date, datetime, timedelta

from babel.dates import format_skeleton
from dateutil.tz import tzlocal
from django.db import models
from django.db.models import Q
from django.template import defaultfilters
from django.utils.timezone import now

from .locale_utils import get_current_locale

ONE_HOUR = timedelta(hours=1)


def full_hours_between(start_time_inclusive, end_time_inclusive, unless=lambda x: False):
    """
    Note that the parameters are start and end inclusive: ie. if you ask for full hours between
    3:00 PM and 5:00 PM, you get 3.00 PM, 4.00 PM and 5.00 PM.
    """
    if any(
        (
            start_time_inclusive.minute,
            start_time_inclusive.second,
            start_time_inclusive.microsecond,
            end_time_inclusive.minute,
            end_time_inclusive.second,
            end_time_inclusive.microsecond,
        )
    ):
        raise ValueError("expecting full hours")

    if start_time_inclusive > end_time_inclusive:
        raise ValueError("start > end")

    result = []

    cur = start_time_inclusive
    while cur <= end_time_inclusive:
        if not unless(cur):
            result.append(cur)
        cur = cur + ONE_HOUR

    return result


def is_within_period(
    period_start: datetime | None,
    period_end: datetime | None,
    t: datetime | None = None,
):
    if t is None:
        t = now()

    return bool(period_start and period_start <= t and not (period_end and period_end <= t))


def get_objects_within_period(
    qs,
    t=None,
    start_field_name="active_from",
    end_field_name="active_until",
    end_field_nullable=True,
    **extra_criteria,
):
    """
    Given a Model with an activity period, return only those instances that are within the
    activity period and match any given extra criteria.

    If the activity period start is not set, the object will never be returned.

    If the activity period end is unset, the object will never expire, ie. will always be
    returned if its activity period start has passed.
    """
    if not isinstance(qs, models.QuerySet):
        qs = qs.objects.all()

    if t is None:
        t = now()

    q = Q(**{f"{start_field_name}__lte": t})

    if end_field_nullable:
        q &= Q(**{f"{end_field_name}__gt": t}) | Q(**{f"{end_field_name}__isnull": True})
    else:
        q &= Q(**{f"{end_field_name}__gt": t})

    q &= Q(**extra_criteria)

    return qs.filter(q)


def format_date_range(
    start_date: date | datetime,
    end_date: date | datetime,
) -> str:
    # FIXME Finnish-specific
    # FIXME should use event.tz but we do not have one for now

    # Special case: Time periods are start inclusive, end exclusive.
    # If an event ends on the first second of a day, it is considered to
    # end at the end of the previous day. This is time zone specific.
    if (
        isinstance(end_date, datetime) and end_date.hour == 0 and end_date.minute == 0 and end_date.second == 0
        # and end_date.microsecond == 0  # microseconds other than 0 are likely user error
    ):
        end_date = end_date - timedelta(seconds=1)

    range_format = "{start_date}–{end_date}"
    if sys.platform == "win32":
        # `strftime` on Windows does not support `%-` formats,
        # for some unfathomable reason.
        full_format = "%d.%m.%Y"
        dm_format = "%d.%m."
        d_format = "%d."
    else:
        full_format = "%-d.%-m.%Y"
        dm_format = "%-d.%-m."
        d_format = "%-d."

    if start_date.year == end_date.year:
        if start_date.month == end_date.month:
            if start_date.day == end_date.day:
                # Y, M, D match
                return start_date.strftime(full_format)
            else:
                # Y, M match, D differ

                return range_format.format(
                    start_date=start_date.strftime(d_format),
                    end_date=end_date.strftime(full_format),
                )
        else:
            # Y match, M, D differ
            return range_format.format(
                start_date=start_date.strftime(dm_format),
                end_date=end_date.strftime(full_format),
            )
    else:
        # Y, M, D differ
        return range_format.format(
            start_date=start_date.strftime(full_format),
            end_date=end_date.strftime(full_format),
        )


def format_interval(
    start_dt,
    end_dt,
    locale=None,
    tz=None,
    date_skeletor="MEd",
    time_skeletor="Hm",
):
    # XXX Finnish-specific
    if tz is None:
        tz = tzlocal()

    if locale is None:
        locale = get_current_locale()

    if start_dt is None:
        return ""

    start_dt = start_dt.astimezone(tz)

    if end_dt is None:
        # be consistent at the expense of making sense in all locales
        interval_format = "{start_date} {start_time}"
        return interval_format.format(
            start_date=format_skeleton(date_skeletor, start_dt, locale=locale),
            start_time=format_skeleton(time_skeletor, start_dt, locale=locale),
        )

    end_dt = end_dt.astimezone(tz)

    if start_dt.date() == end_dt.date():
        interval_format = "{start_date} {start_time}–{end_time}"
    else:
        interval_format = "{start_date} {start_time} – {end_date} {end_time}"

    return interval_format.format(
        start_date=format_skeleton(date_skeletor, start_dt, locale=locale),
        start_time=format_skeleton(time_skeletor, start_dt, locale=locale),
        end_date=format_skeleton(date_skeletor, end_dt, locale=locale),
        end_time=format_skeleton(time_skeletor, end_dt, locale=locale),
    )


def format_date(date):
    if date is None:
        return ""

    return defaultfilters.date(date, "SHORT_DATE_FORMAT")


def format_datetime(datetime):
    if datetime is None:
        return ""

    tz = tzlocal()
    return defaultfilters.date(datetime.astimezone(tz), "SHORT_DATETIME_FORMAT")


# http://stackoverflow.com/a/9754466
def calculate_age(born, today):
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
