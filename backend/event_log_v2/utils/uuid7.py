"""
As of 2024-07-30, the uuid7 module at https://github.com/stevesimmons/uuid7
incorrectly uses seconds and not milliseconds as the timestamp part of the UUIDv7.

This code is based on https://antonz.org/uuidv7/#python and uses milliseconds.

Spec https://www.rfc-editor.org/rfc/rfc9562#name-uuid-version-7
"""

import os
import time
from datetime import UTC, datetime
from uuid import UUID


def uuid7(timestamp: datetime | None = None, zero: bool = False) -> UUID:
    # random bytes
    if zero:
        value = bytearray(16)
    else:
        value = bytearray(os.urandom(16))

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


def uuid7_range_for_month(year: int, month: int):
    start = datetime(year, month, 1, tzinfo=UTC)
    december = 12
    end = (
        start.replace(month=start.month + 1) if start.month < december else start.replace(year=start.year + 1, month=1)
    )

    return uuid7(start, zero=True), uuid7(end, zero=True)


def uuid7_to_datetime(uuid: UUID) -> datetime:
    ms = uuid.int >> 80
    return datetime.fromtimestamp(ms / 1000, tz=UTC)
