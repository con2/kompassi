from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from ..models.order import Order, OrderOwner
from ..models.receipts import Receipt


@login_required
def etickets_view(request: HttpRequest, event_slug: str, order_id: str) -> HttpResponse:
    # TODO admin access to tickets
    try:
        order = OrderOwner.get_user_order(
            event_slug=event_slug,
            order_id=order_id,
            user_id=request.user.id,  # type: ignore
        )
    except Order.DoesNotExist:
        return HttpResponse("Order not found or not accessible by you", status=400)

    receipt = Receipt.from_order(order)
    if not receipt:
        return HttpResponse("Order is not paid", status=400)

    etickets_pdf = receipt.get_etickets_pdf()
    if not etickets_pdf:
        return HttpResponse("Order does not contain electronic tickets", status=400)

    return HttpResponse(etickets_pdf, content_type="application/pdf")
