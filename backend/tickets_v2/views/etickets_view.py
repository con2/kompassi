from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from ..models.order import Order
from ..models.receipt import PendingReceipt


@login_required
def etickets_view(request: HttpRequest, event_slug: str, order_id: str) -> HttpResponse:
    try:
        order = Order.objects.get(
            event__slug=event_slug,
            id=order_id,
            owner=request.user,
        )
    except Order.DoesNotExist:
        return HttpResponse("Order not found or not accessible by you", status=400)

    receipt = PendingReceipt.from_order(order)
    if not receipt:
        return HttpResponse("Order is not paid", status=400)

    etickets_pdf = receipt.get_etickets_pdf()
    if not etickets_pdf:
        return HttpResponse("Order does not contain electronic tickets", status=400)

    return HttpResponse(etickets_pdf, content_type="application/pdf")
