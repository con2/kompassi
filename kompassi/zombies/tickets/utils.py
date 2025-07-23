from datetime import date as date_type
from datetime import datetime
from decimal import Decimal

from kompassi.tickets_v2.optimized_server.utils.formatting import format_money


def format_price(cents: int) -> str:
    if isinstance(cents, Decimal):
        raise AssertionError(
            "Suspect Decimal input may be passed in euros where cents are expected. "
            "Cast to int to convince `format_price` input is cents."
        )

    return format_money(Decimal(cents) / 100)


def format_date(dt: date_type | datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def append_reference_number_checksum(s: str) -> str:
    return s + str(-sum(int(x) * [7, 3, 1][i % 3] for i, x in enumerate(s[::-1])) % 10)
