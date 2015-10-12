# encoding: utf-8

import sys
from datetime import date, datetime, timedelta

from django.utils.timezone import now
from django.template import defaultfilters


ONE_HOUR = timedelta(hours=1)


def full_hours_between(start_time_inclusive, end_time_inclusive, unless=lambda x: False):
    """
    Note that the parameters are start and end inclusive: ie. if you ask for full hours between
    3:00 PM and 5:00 PM, you get 3.00 PM, 4.00 PM and 5.00 PM.
    """
    if any((
        start_time_inclusive.minute,
        start_time_inclusive.second,
        start_time_inclusive.microsecond,
        end_time_inclusive.minute,
        end_time_inclusive.second,
        end_time_inclusive.microsecond
    )):
        raise ValueError('expecting full hours')

    if start_time_inclusive > end_time_inclusive:
        raise ValueError('start > end')

    result = []

    cur = start_time_inclusive
    while cur <= end_time_inclusive:
        if not unless(cur):
            result.append(cur)
        cur = cur + ONE_HOUR

    return result


def is_within_period(period_start, period_end, t=None):
    if t is None:
        t = now()

    return period_start and period_start <= t and \
        not (period_end and period_end <= t)


def format_date_range(start_date, end_date):
    # XXX Finnish-specific

    range_format = u"{start_date}–{end_date}"
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
                end_date=end_date.strftime(full_format)
            )
    else:
        # Y, M, D differ
        return range_format.format(
            start_date=start_date.strftime(full_format),
            end_date=end_date.strftime(full_format),
        )


def format_date(date):
    return defaultfilters.date(date, "SHORT_DATE_FORMAT")


def format_datetime(datetime):
    tz = tzlocal()
    return defaultfilters.date(datetime.astimezone(tz), "SHORT_DATETIME_FORMAT")
