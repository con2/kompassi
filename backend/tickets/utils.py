from datetime import date as date_type
from datetime import datetime


def format_price(cents: int) -> str:
    return "%d,%02d €" % divmod(cents, 100)


def format_date(dt: date_type | datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def append_reference_number_checksum(s: str) -> str:
    return s + str(-sum(int(x) * [7, 3, 1][i % 3] for i, x in enumerate(s[::-1])) % 10)
