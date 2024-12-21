from datetime import date as date_type
from datetime import datetime
from decimal import Decimal


def format_money(euros: Decimal) -> str:
    """
    >>> format_money(Decimal('123.45'))
    '123,45 €'
    """
    if isinstance(euros, int):
        raise AssertionError(
            "Suspect integer input may be passed in cents where euros are expected. "
            "Cast to Decimal to convince `format_money` input is euros."
        )

    return f"{euros:0.2f} €".replace(".", ",")


def format_order_number(order_number: int):
    """
    >>> format_order_number(423125)
    '#423125'
    >>> format_order_number(1231231)
    '#1231231'
    """
    return f"#{order_number:06d}"


def order_number_to_reference(order_date: date_type | datetime, order_number: int):
    """
    >>> order_number_to_reference(date_type(2021, 1, 1), 1231231)
    '2021012312310'
    """
    return append_reference_number_checksum(f"{order_date.year}{order_number:07d}")


def append_reference_number_checksum(s: str) -> str:
    """
    >>> append_reference_number_checksum('8888888')
    '88888888'
    """
    return s + str(-sum(int(x) * [7, 3, 1][i % 3] for i, x in enumerate(s[::-1])) % 10)
