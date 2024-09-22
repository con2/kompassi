"""
NOTE: Also implemented in FastAPI/Uvicorn for SPEED. See ../optimized_server.
"""

import pydantic
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.models.event import Event

from ..optimized_server.excs import NotEnoughTickets
from ..optimized_server.models.order import Order
from ..optimized_server.models.product import Product


@cache_page(1)
def get_products(_request: HttpRequest, event_slug: str) -> JsonResponse:
    event = get_object_or_404(Event, slug=event_slug)
    products_with_availability = Product.get_products_django(event.id)
    return JsonResponse(
        {
            "event": dict(name=event.name),
            "products": [
                {
                    "id": product.id,
                    "title": product.title,
                    "description": product.description,
                    "price": product.price,
                    "available": product.available,
                }
                for product in products_with_availability
            ],
        },
    )


@require_POST
@csrf_exempt  # TODO
def create_order(request: HttpRequest, event_slug: str) -> JsonResponse:
    try:
        order_dto = Order.model_validate_json(request.body)
    except pydantic.ValidationError:
        return JsonResponse(dict(code=400, message="Bad request"), status=400)

    try:
        with transaction.atomic():
            event = get_object_or_404(Event, slug=event_slug)
            order_id = order_dto.save_django(event.id)
            # payment = CheckoutPayment.from_order_v2(order)
            # payment.save()
    except NotEnoughTickets:
        return JsonResponse(dict(code=409, message="Conflict"), status=409)

    # response = payment.perform_create_payment_request(request)

    return JsonResponse(
        {
            "order_id": order_id,
            # payment_redirect=response["href"],
            "payment_redirect": "",
        },
    )
