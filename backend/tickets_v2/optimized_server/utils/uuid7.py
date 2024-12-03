"""
As of 2024-07-30, the uuid7 module at https://github.com/stevesimmons/uuid7
incorrectly uses seconds and not milliseconds as the timestamp part of the UUIDv7.

This code is based on https://antonz.org/uuidv7/#python and uses milliseconds.

Spec https://www.rfc-editor.org/rfc/rfc9562#name-uuid-version-7
"""

from __future__ import annotations

import os
import time
from datetime import UTC, datetime, timedelta
from datetime import date as date_type
from datetime import time as time_type
from uuid import UUID


def uuid7(timestamp: datetime | None = None, rand: int | None = None) -> UUID:
    """
    Generate an UUIDv7. By default the random part will be, well, random.

    If you really know what you are doing, you can try to use timestamp and rand to
    deterministically create an UUIDv7. The unsigned representation of `rand`
    must fit in 8 bytes.
    """
    # random bytes
    if rand is None:
        value = bytearray(os.urandom(16))
    else:
        value = bytearray(bytes(8) + rand.to_bytes(8, signed=False, byteorder="big"))

    if timestamp is None:
        # current timestamp in ms
        ms = int(time.time() * 1000)
    else:
        ms = int(timestamp.timestamp() * 1000)

    # timestamp
    value[0] = (ms >> 40) & 0xFF
    value[1] = (ms >> 32) & 0xFF
    value[2] = (ms >> 24) & 0xFF
    value[3] = (ms >> 16) & 0xFF
    value[4] = (ms >> 8) & 0xFF
    value[5] = ms & 0xFF

    # version and variant
    value[6] = (value[6] & 0x0F) | 0x70
    value[8] = (value[8] & 0x3F) | 0x80

    return UUID(bytes=bytes(value))


def uuid7_month_range_for_year_month(year: int, month: int) -> tuple[UUID, UUID]:
    start = datetime(year, month, 1, tzinfo=UTC)
    december = 12
    end = (
        start.replace(month=start.month + 1) if start.month < december else start.replace(year=start.year + 1, month=1)
    )

    return uuid7(start, rand=0), uuid7(end, rand=0)


def uuid7_month_range(d: datetime | date_type):
    if isinstance(d, datetime):
        d = d.date()

    return uuid7_month_range_for_year_month(d.year, d.month)


def uuid7_day_range(d: datetime | date_type):
    if isinstance(d, datetime):
        d = d.date()

    start = datetime.combine(d, time_type(0), tzinfo=UTC)
    end = start + timedelta(days=1)

    return uuid7(start, rand=0), uuid7(end, rand=0)


def uuid7_to_datetime(uuid: UUID) -> datetime:
    ms = uuid.int >> 80
    return datetime.fromtimestamp(ms / 1000, tz=UTC)


def uuid7_year_range(year: int) -> tuple[UUID, UUID]:
    start = datetime(year, 1, 1, tzinfo=UTC)
    end = datetime(year + 1, 1, 1, tzinfo=UTC)

    return uuid7(start, rand=0), uuid7(end, rand=0)
