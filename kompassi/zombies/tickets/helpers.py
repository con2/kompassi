from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import get_ip

from .models import Order

__all__ = [
    "clear_order",
    "complete_phase",
    "destroy_order",
    "get_order",
    "is_phase_completed",
    "set_order",
    "tickets_admin_required",
    "tickets_event_required",
]


ORDER_KEY_TEMPLATE = "{event.slug}.tickets.order_id"
PHASE_KEY_TEMPLATE = "{event.slug}.tickets.phases"


def set_order(request, event, order):
    order_key = ORDER_KEY_TEMPLATE.format(event=event)
    request.session[order_key] = order.pk


def get_order(request, event):
    order_key = ORDER_KEY_TEMPLATE.format(event=event)
    order_id = request.session.get(order_key)

    if order_id is not None:
        # There is an order in the session; return it
        try:
            return Order.objects.get(
                id=order_id,
                event=event,
                cancellation_time__isnull=True,
            )
        except Order.DoesNotExist:
            clear_order(request, event)

    # No order in the session; return an unsaved order
    return Order(
        event=event,
        ip_address=get_ip(request) or "",
        language=get_language(),
    )


def clear_order(request, event):
    order_key = ORDER_KEY_TEMPLATE.format(event=event)
    if order_key in request.session:
        del request.session[order_key]

    phase_key = PHASE_KEY_TEMPLATE.format(event=event)
    if phase_key in request.session:
        del request.session[phase_key]


def destroy_order(request, event):
    order = get_order(request, event)
    if order.pk is None:
        return

    if order.is_confirmed:
        order.cancel(send_email=False)
    else:
        if order.customer:
            order.customer.delete()
        order.order_product_set.all().delete()
        order.delete()

    clear_order(request, event)


def is_phase_completed(request, event, phase):
    phase_key = PHASE_KEY_TEMPLATE.format(event=event)
    completed_phases = request.session.get(phase_key, [])
    return phase in completed_phases


def complete_phase(request, event, phase):
    phase_key = PHASE_KEY_TEMPLATE.format(event=event)
    completed_phases = request.session.get(phase_key, [])
    completed_phases = set(completed_phases)
    completed_phases.add(phase)
    request.session[phase_key] = list(completed_phases)


SEARCH_CRITERIA_MAP = dict(
    id="id",
    first_name="customer__first_name__icontains",
    last_name="customer__last_name__icontains",
    email="customer__email__icontains",
)


def perform_search(event, **kwargs):
    criteria = {SEARCH_CRITERIA_MAP[k]: v for (k, v) in kwargs.items() if v}
    return event.order_set.filter(confirm_time__isnull=False, **criteria).order_by("-confirm_time")


def tickets_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        from kompassi.core.models import Event
        from kompassi.core.utils import login_redirect

        from .views import tickets_admin_menu_items

        event = get_object_or_404(Event, slug=event_slug)
        meta = event.tickets_event_meta

        if not meta:
            messages.error(request, _("This event does not use Kompassi for ticket sales."))
            return redirect("core_event_view", event.slug)

        if not meta.is_user_admin(request.user):
            return login_redirect(request)

        vars = dict(
            event=event,
            admin_menu_items=tickets_admin_menu_items(request, event),
            admin_title="Lipunmyynnin hallinta",
        )

        return view_func(request, vars, event, *args, **kwargs)

    return wrapper


def tickets_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        from kompassi.core.models import Event

        event = get_object_or_404(Event, slug=event_slug)
        meta = event.tickets_event_meta

        if not meta:
            messages.error(request, _("This event does not use Kompassi for ticket sales."))
            return redirect("core_event_view", event.slug)

        if not (meta.is_ticket_sales_open or meta.is_user_admin(request.user)):
            messages.error(request, _("Ticket sales for this event has not yet started."))
            return redirect("core_event_view", event.slug)

        return view_func(request, event, *args, **kwargs)

    return wrapper
