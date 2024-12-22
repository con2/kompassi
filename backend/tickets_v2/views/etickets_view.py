from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from access.cbac import is_graphql_allowed
from core.models.event import Event

from ..models.order import Order
from ..models.receipt import PendingReceipt
from ..optimized_server.models.enums import PaymentStatus


@login_required
def etickets_view(request: HttpRequest, event_slug: str, order_id: str) -> HttpResponse:
    event = get_object_or_404(Event, slug=event_slug)

    try:
        UUID(order_id)
    except ValueError:
        return HttpResponse("Invalid order ID", status=400)

    queryset = Order.objects.filter(
        event=event,
        id=order_id,
    )

    if not is_graphql_allowed(
        request.user,
        scope=event.scope,
        operation="query",
        app="tickets_v2",
        model="Order",
        field="etickets_pdf",
        id=order_id,
    ):
        queryset = queryset.filter(owner=request.user)

    try:
        order = queryset.get()
    except Order.DoesNotExist:
        return HttpResponse("Order not found or not accessible by you", status=400)

    if order.cached_status != PaymentStatus.PAID:
        return HttpResponse("Order is unpaid or cancelled", status=400)

    etickets_pdf = PendingReceipt.from_order(order).get_etickets_pdf()
    if not etickets_pdf:
        return HttpResponse("Order does not contain electronic tickets", status=400)

    return HttpResponse(etickets_pdf, content_type="application/pdf")
