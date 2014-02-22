# encoding: utf-8

from datetime import date
import re

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Order, OrderProduct


__all__ = [
    "redirect",
    "set_order",
    "get_order",
    "clear_order",
    "destroy_order",
    "is_soldout",
    "is_phase_completed",
    "complete_phase"
]


ORDER_KEY_TEMPLATE = "{event.slug}.tickets.order_id"
PHASE_KEY_TEMPLATE = "{event.slug}.tickets.phases"


def redirect(view_name, **kwargs):
    return HttpResponseRedirect(reverse(view_name, kwargs=kwargs))


def set_order(request, event, order):
    order_key = ORDER_KEY_TEMPLATE.format(event=event)
    request.session[order_key] = order.pk


def get_order(request, event):
    order_key = ORDER_KEY_TEMPLATE.format(event=event)
    order_id = request.session.get(order_key)

    if order_id is not None:
        # There is an order in the session; return it
        return Order.objects.get(id=order_id)
    else:
        # No order in the session; return an unsaved order
        return Order(event=event, ip_address=request.META.get("REMOTE_ADDR"))


def clear_order(request, event):
    order_key = ORDER_KEY_TEMPLATE.format(event=event)
    if request.session.has_key(order_key):
        del request.session[order_key]

    phase_key = PHASE_KEY_TEMPLATE.format(event=event)
    if request.session.has_key(phase_key):
        del request.session[phase_key]


def destroy_order(request, event):
    order = get_order(request, event)
    if order.pk is None:
        return

    order.order_product_set.all().delete()

    if order.customer:
        order.customer.delete()

    order.delete()
    clear_order(request, event)


# XXX
def is_soldout(productdata):
    for (product, amount) in productdata.iteritems():
        if (product.amount_available < amount):
            return True
    return False


def is_phase_completed(request, event, phase):
    phase_key = PHASE_KEY_TEMPLATE.format(event=event)
    completed_phases = request.session.get(phase_key, set())
    return phase in completed_phases


def complete_phase(request, event, phase):
    phase_key = PHASE_KEY_TEMPLATE.format(event=event)
    completed_phases = request.session.get(phase_key, set())
    completed_phases.add(phase)
    request.session[phase_key] = completed_phases


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


def get_order_by_ref(event, ref):
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

    order = event.order_set.get(id=order_id)

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


def perform_search(event, **kwargs):
    criteria = dict((SEARCH_CRITERIA_MAP[k], v) for (k, v) in kwargs.iteritems() if v)
    return event.order_set.filter(
        confirm_time__isnull=False,
        **criteria
    ).order_by('-confirm_time')


def tickets_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event, *args, **kwargs):
        from core.models import Event
        from core.utils import login_redirect
        from .views import tickets_admin_menu_items

        event = get_object_or_404(Event, slug=event)
        meta = event.tickets_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Turskaa työvoiman hallintaan.")
            return redirect('core_event_view', event.slug)

        if not event.tickets_event_meta.is_user_admin(request.user):
            return login_redirect(request)

        vars = dict(
            event=event,
            admin_menu_items=tickets_admin_menu_items(request, event)
        )

        return view_func(request, vars, event, *args, **kwargs)
    return wrapper


def tickets_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event, *args, **kwargs):
        from core.models import Event

        event = get_object_or_404(Event, slug=event)
        meta = event.tickets_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Turskaa työvoiman hallintaan.")
            return redirect('core_event_view', event.slug)

        return view_func(request, event, *args, **kwargs)
    return wrapper
