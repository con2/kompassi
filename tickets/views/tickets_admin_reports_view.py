from django.shortcuts import render

from ..helpers import tickets_admin_required
from ..models import Order, ProductHandout


@tickets_admin_required
def tickets_admin_reports_view(request, vars, event):
    vars.update(
        product_handouts=ProductHandout.get_product_handouts(event),
        arrivals_by_hour=Order.get_arrivals_by_hour(event),
    )

    return render(request, "tickets_admin_reports_view.pug", vars)
