from typing import Any, Literal

from django.db import models
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.timezone import now

from core.csv_export import EXPORT_FORMATS, csv_response
from core.models import Event

from ..helpers import tickets_admin_required
from ..models import (
    Order,
    OrderProduct,
)


def product_filter(request: HttpRequest, queryset: models.QuerySet[OrderProduct]) -> models.QuerySet[OrderProduct]:
    queryset = queryset.filter(count__gte=1)

    products_str = request.GET.get("products")
    if not products_str:
        return queryset

    products = [int(i) for i in products_str.split(",")]
    return queryset.filter(product__in=products)


@tickets_admin_required
def tickets_admin_export_view(
    request: HttpRequest,
    vars: dict[str, Any],
    event: Event,
    format="xlsx",
):
    ops = OrderProduct.objects.filter(
        order__event=event,
        # Order is confirmed
        order__confirm_time__isnull=False,
        # Order is paid
        order__payment_date__isnull=False,
        # Order is not cancelled
        order__cancellation_time__isnull=True,
    )
    ops = product_filter(request, ops)
    ops = ops.order_by("order__payment_date", "id")

    timestamp = now().strftime("%Y%m%d%H%M%S")

    return csv_response(
        event,
        OrderProduct,
        ops,
        dialect=next(fmt for fmt in EXPORT_FORMATS if fmt.extension == format).csv_dialect,
        filename=f"{event.slug}_ticketsales_{timestamp}.{format}",
    )


@tickets_admin_required
def tickets_admin_paulig_export_view(
    request: HttpRequest,
    vars: dict[str, Any],
    event: Event,
    format: Literal["html"] = "html",
):
    """
    Useful for eg. delivering intermission orders to Tampere-talo catering.
    """
    orders = Order.objects.filter(
        event=event,
        # Order is confirmed
        confirm_time__isnull=False,
        # Order is paid
        payment_date__isnull=False,
        # Order is not cancelled
        cancellation_time__isnull=True,
    ).order_by("customer__last_name", "customer__first_name")

    orders_with_filtered_products = [
        (order, filtered_products)
        for order in orders
        if (filtered_products := product_filter(request, order.order_product_set.all()))
    ]

    vars.update(
        orders_with_filtered_products=orders_with_filtered_products,
    )

    return render(request, "tickets_admin_paulig_export_view.pug", vars)
