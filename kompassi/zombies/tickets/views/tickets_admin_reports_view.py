from django.shortcuts import render

from kompassi.payments.models import CheckoutPayment

from ..helpers import tickets_admin_required
from ..models import Order, ProductHandout


@tickets_admin_required
def tickets_admin_reports_view(request, vars, event):
    vars.update(
        arrivals_by_hour=Order.get_arrivals_by_hour(event),
        orders_by_payment_status=CheckoutPayment.get_orders_by_payment_status(event),
        payments_by_payment_method=CheckoutPayment.get_payments_by_payment_method(event),
        product_handouts=ProductHandout.get_product_handouts(event),
    )

    return render(request, "tickets_admin_reports_view.pug", vars)
