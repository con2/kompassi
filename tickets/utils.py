# encoding: utf-8
# vim: shiftwidth=4 expandtab

from ticket_sales.models import Order, OrderProduct

from datetime import date
import re

PAYMENT_REGEX = re.compile(
    # Date field
    r'(?P<day>\d+)\.(?P<month>\d+)\.(?P<year>\d+)\s+' +

    # Payer name field
    r'(?P<name>.+?)\s+' +

    # The word "VIITESIIRTO", marking this as a reference number payment
    r'VIITESIIRTO\s+' +

    # Reference number field
    r'(?P<ref>(\d+\s)*\d+)\s+' +

    # Sum of the payment
    r'(?P<euros>\d+),(?P<cents>\d+)'
)

class ParseResult(object):
    OK = "ok"

    NO_MATCH = "no_match"
    ORDER_NOT_FOUND = "order_not_found"
    ORDER_NOT_CONFIRMED = "order_not_confirmed"
    PAYMENT_ALREADY_CONFIRMED = "payment_already_confirmed"
    SUM_MISMATCH = "sum_mismatch"

def parse_payments(lines):
    """parse_payments(lines) -> gen[(line, result, date, order)]

    Parses payments from a copy-paste dump extracted from the e-bank.
    """

    for line in lines:
        yield parse_payment(line)

def parse_payment(line):
    # Test #1: Can be parsed by PAYMENT_REGEX
    match = PAYMENT_REGEX.match(line)
    if match is None:
        return line, ParseResult.NO_MATCH, None, None

    # Assemble the payment date
    year = int(match.group("year"))
    month = int(match.group("month"))
    day = int(match.group("day"))
    payment_date = date(year=year, month=month, day=day)

    # Test #2: An order is found by the reference number
    ref = match.group("ref")
    try:
        order = get_order_by_ref(ref)
    except Order.DoesNotExist:
        return line, ParseResult.ORDER_NOT_FOUND, payment_date, None

    # Test #3: The order has been confirmed
    if not order.is_confirmed:
        return line, ParseResult.ORDER_NOT_CONFIRMED, order

    # Test #4: The order has not yet been marked as paid
    if order.is_paid:
        return line, ParseResult.PAYMENT_ALREADY_CONFIRMED, payment_date, order

    # Test #5: The sum matches that of the order
    euros = match.group("euros")
    cents = match.group("cents")
    total_cents = int(cents) + 100 * int(euros)
    if total_cents != order.price_cents:
        return line, ParseResult.SUM_MISMATCH, payment_date, order

    # If all tests passed, the order is ready to be marked as paid.
    return line, ParseResult.OK, payment_date, order

def normalize_ref(ref):
    return "".join(i for i in ref if i.isdigit())

def get_order_by_ref(ref):
    """get_order_by_ref(ref) -> Order

    Raises Order.DoesNotExist on failature."""
    ref = normalize_ref(ref)
    
    # XXX hard-coded format in here and models.Order.reference_number_base
    if not ref.startswith("5"):
        raise Order.DoesNotExist

    # XXX hard-coded length in here and models.Order.reference_number_base
    if len(ref) != 6:
        raise Order.DoesNotExist

    # Lose the prefix and checksum
    order_id = int(ref[1:-1])

    order = Order.objects.get(id=order_id)

    # Final validation check
    if ref != order.reference_number:
        raise Order.DoesNotExist

    return order

SEARCH_CRITERIA_MAP = dict(
    id="id",
    first_name="customer__first_name__icontains",
    last_name="customer__last_name__icontains",
    email="customer__email__icontains"
)

def perform_search(**kwargs):
    criteria = dict((SEARCH_CRITERIA_MAP[k], v)
        for (k, v) in kwargs.iteritems() if v)
    return Order.objects.filter(
        confirm_time__isnull=False,
        **criteria
    ).order_by('-confirm_time')
