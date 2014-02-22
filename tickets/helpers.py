# encoding: utf-8
# vim: shiftwidth=4 expandtab

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from ticket_sales.models import Order, OrderProduct

__all__ = [
    "redirect",
    "set_order",
    "get_order",
    "clear_order",
    "destroy_order",
    "init_form",
    "is_soldout",
    "is_phase_completed",
    "complete_phase"
]

ORDER_KEY = "ticket_sales.order_id"
PHASE_KEY = "ticket_sales.phases"

def redirect(view_name, **kwargs):
    return HttpResponseRedirect(reverse(view_name, kwargs=kwargs))

def set_order(request, order):
    request.session[ORDER_KEY] = order.pk

def get_order(request):
    order_id = request.session.get(ORDER_KEY)

    if order_id is not None:
        # There is an order in the session; return it
        return Order.objects.get(id=order_id)
    else:
        # No order in the session; return an unsaved order
        return Order(ip_address=request.META.get("REMOTE_ADDR"))

def clear_order(request):
    if request.session.has_key(ORDER_KEY):
        del request.session[ORDER_KEY]

    if request.session.has_key(PHASE_KEY):
        del request.session[PHASE_KEY]

def destroy_order(request):
    order = get_order(request)
    if order.pk is None:
        return
    
    order.order_product_set.all().delete()

    if order.customer:
        order.customer.delete()

    order.delete()
    clear_order(request)

def init_form(form_class, request, instance=None, prefix=None):
    args = []
    kwargs = {}

    if request.method == "POST":
        args.append(request.POST)
    if instance is not None:
        kwargs["instance"] = instance
    if prefix is not None:
        kwargs["prefix"] = prefix

    return form_class(*args, **kwargs)

def is_soldout(productdata):
    for (product, amount) in productdata.iteritems():
        if (product.amount_available < amount):
            return True
    return False 

def is_phase_completed(request, phase):
    completed_phases = request.session.get(PHASE_KEY, set())
    return phase in completed_phases

def complete_phase(request, phase):
    completed_phases = request.session.get(PHASE_KEY, set())
    completed_phases.add(phase)
    request.session[PHASE_KEY] = completed_phases
