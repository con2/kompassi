import logging
from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, HTTPException, Path

from .db import DB, lifespan
from .excs import InvalidProducts, NotEnoughTickets
from .models.api import PayOrderRequest
from .models.enums import PaymentProvider
from .models.event import Event
from .models.order import CreateOrderRequest, Order, OrderWithCustomer
from .models.product import Product
from .services.paytrail import CreatePaymentRequest

app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)


EventSlug = Annotated[str, Path()]
OrderId = Annotated[UUID, Path()]


@app.get("/api/tickets-v2/status/")
async def status():
    return {"status": "OK"}


@app.get("/api/tickets-v2/{event_slug}/products/")
async def get_products(event_slug: EventSlug, db: DB):
    event = await Event.get(db, event_slug)
    if event is None:
        raise HTTPException(status_code=400, detail="EVENT_NOT_FOUND")

    products = await Product.get_products(db, event.id)

    return {
        "event": {
            "name": event.name,
        },
        "products": [product.model_dump() for product in products],
    }


@app.post("/api/tickets-v2/{event_slug}/orders/")
async def create_order(event_slug: EventSlug, order: CreateOrderRequest, db: DB):
    event = await Event.get(db, event_slug)
    if event is None:
        raise HTTPException(status_code=400, detail="INVALID_ORDER")

    try:
        async with db.transaction():
            result = await order.save(db, event.id)
    except NotEnoughTickets as e:
        raise HTTPException(409, "NOT_ENOUGH_TICKETS") from e
    except InvalidProducts as e:
        raise HTTPException(400, "INVALID_ORDER") from e

    payment_redirect = ""
    match event.provider:
        case PaymentProvider.NONE:
            if result.total_price > 0:
                logger.error("Order %s has non-zero price with no payment provider", result.order_id)
                raise HTTPException(400, "INVALID_ORDER")
        case PaymentProvider.PAYTRAIL:
            request = CreatePaymentRequest.from_create_order_request(event, order, result)
            response = await request.send(db, event, result.order_id)
            payment_redirect = response.href
        case _:
            logger.error("Payment provider not implemented: %s", event.provider)
            raise HTTPException(400, "INVALID_ORDER")

    return {
        "orderId": result.order_id,
        "paymentRedirect": payment_redirect,
    }


@app.get("/api/tickets-v2/{event_slug}/orders/{order_id}/")
async def get_order(event_slug: EventSlug, order_id: OrderId, db: DB):
    event = await Event.get(db, event_slug)
    if event is None:
        raise HTTPException(status_code=400, detail="EVENT_NOT_FOUND")

    order = await Order.get(db, event.id, order_id)
    if order is None:
        raise HTTPException(status_code=400, detail="ORDER_NOT_FOUND")

    return {
        "event": {
            "name": event.name,
        },
        "order": order.model_dump(mode="json", by_alias=True),
    }


@app.post("/api/tickets-v2/{event_slug}/orders/{order_id}/payment/")
async def pay(
    event_slug: EventSlug,
    order_id: OrderId,
    pay_order_request: PayOrderRequest,
    db: DB,
):
    event = await Event.get(db, event_slug)
    if event is None:
        raise HTTPException(status_code=400, detail="EVENT_NOT_FOUND")

    order = await OrderWithCustomer.get(db, event.id, order_id)
    if order is None:
        raise HTTPException(status_code=400, detail="ORDER_NOT_FOUND")

    payment_redirect = ""
    match event.provider:
        case PaymentProvider.PAYTRAIL:
            request = CreatePaymentRequest.from_order(event, order, pay_order_request.language)
            response = await request.send(db, event, order_id)
            payment_redirect = response.href

    if not payment_redirect:
        raise HTTPException(status_code=400, detail="INVALID_ORDER")

    return {
        "orderId": order.id,
        "paymentRedirect": payment_redirect,
    }
