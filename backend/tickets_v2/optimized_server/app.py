import logging
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Path
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse

from .db import DB, lifespan
from .excs import InvalidProducts, NotEnoughTickets
from .models.api import PayOrderRequest
from .models.enums import PaymentProvider, PaymentStampType
from .models.event import Event
from .models.order import CreateOrderRequest, Order, OrderWithCustomer
from .models.payment_stamp import PaymentStamp
from .models.product import Product
from .services.paytrail import CreatePaymentRequest, PaymentCallback

app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)

EventSlug = Annotated[str, Path()]
OrderId = Annotated[UUID, Path()]


async def _event(event_slug: EventSlug, db: DB) -> Event:
    event = await Event.get(db, event_slug)
    if event is None:
        raise HTTPException(status_code=400, detail="EVENT_NOT_FOUND")
    return event


_Event = Annotated[Event, Depends(_event)]


async def _order(event: _Event, order_id: OrderId, db: DB) -> Order:
    order = await Order.get(db, event.id, order_id)
    if order is None:
        raise HTTPException(status_code=400, detail="ORDER_NOT_FOUND")
    return order


_Order = Annotated[Order, Depends(_order)]


async def _order_with_customer(event: _Event, order_id: OrderId, db: DB) -> OrderWithCustomer:
    order = await OrderWithCustomer.get(db, event.id, order_id)
    if order is None:
        raise HTTPException(status_code=400, detail="ORDER_NOT_FOUND")
    return order


_OrderWithCustomer = Annotated[OrderWithCustomer, Depends(_order_with_customer)]


@app.get("/api/tickets-v2/status/")
async def status():
    return {"status": "OK"}


@app.get("/api/tickets-v2/{event_slug}/products/")
async def get_products(event: _Event, db: DB):
    products = await Product.get_products(db, event.id)

    return {
        "event": {
            "name": event.name,
        },
        "products": [product.model_dump() for product in products],
    }


@app.post("/api/tickets-v2/{event_slug}/orders/")
async def create_order(event: _Event, order: CreateOrderRequest, db: DB):
    try:
        async with db.transaction():
            result = await order.save(db, event.id)
    except NotEnoughTickets as e:
        raise HTTPException(409, "NOT_ENOUGH_TICKETS") from e
    except InvalidProducts as e:
        raise HTTPException(400, "INVALID_ORDER") from e

    payment_redirect = ""
    stamps = []

    if result.total_price > 0:
        match event.provider:
            case PaymentProvider.NONE:
                logger.error("New order %s has non-zero price with no payment provider", result.order_id)
                raise HTTPException(400, "INVALID_ORDER")
            case PaymentProvider.PAYTRAIL:
                request = CreatePaymentRequest.from_create_order_request(event, order, result)
                response, stamps = await request.send(event, result.order_id)
                payment_redirect = response.href
            case _:
                logger.error("Payment provider not implemented: %s", event.provider)
                raise HTTPException(400, "INVALID_ORDER")
    elif result.total_price == 0:
        stamps.append(PaymentStamp.for_zero_price_order(event, result.order_id))
    else:
        logger.error("New order %s has negative price", result.order_id)
        raise HTTPException(400, "INVALID_ORDER")

    async with db.transaction():
        await PaymentStamp.save_many(db, stamps)

    return {
        "orderId": result.order_id,
        "paymentRedirect": payment_redirect,
    }


@app.get("/api/tickets-v2/{event_slug}/orders/{order_id}/")
async def get_order(event: _Event, order: _Order):
    return {
        "event": {
            "name": event.name,
        },
        "order": order.model_dump(mode="json", by_alias=True),
    }


@app.post("/api/tickets-v2/{event_slug}/orders/{order_id}/payment/")
async def pay(
    event: _Event,
    order: _OrderWithCustomer,
    pay_order_request: PayOrderRequest,
    db: DB,
):
    payment_redirect = ""
    stamps = []

    if order.total_price <= 0:
        logger.error("Asked to pay for existing order %s with nonpositive price", order.id)
        raise HTTPException(status_code=400, detail="INVALID_ORDER")

    match event.provider:
        case PaymentProvider.PAYTRAIL:
            request = CreatePaymentRequest.from_order(event, order, pay_order_request.language)
            response, stamps = await request.send(event, order.id)
            payment_redirect = response.href
        case PaymentProvider.NONE:
            logger.error("Asked to pay for existing order %s with nonzero price but no payment provider", order.id)
            raise HTTPException(status_code=400, detail="INVALID_ORDER")
        case _:
            logger.error("Payment provider not implemented: %s (order %s)", event.provider, order.id)
            raise HTTPException(400, "INVALID_ORDER")

    async with db.transaction():
        await PaymentStamp.save_many(db, stamps)

    if not payment_redirect:
        logger.error("Payment method did not return a redirect URL for order %s", order.id)
        raise HTTPException(status_code=400, detail="INVALID_ORDER")

    return {
        "orderId": order.id,
        "paymentRedirect": payment_redirect,
    }


def valid_callback(event: _Event, request: Request) -> PaymentCallback:
    return PaymentCallback.from_query_params(request.query_params, event)


_Callback = Annotated[PaymentCallback, Depends(valid_callback)]


@app.get("/api/tickets-v2/{event_slug}/orders/{order_id}/redirect/")
async def paytrail_redirect(
    event: _Event,
    order: _Order,
    paytrail_callback: _Callback,
    db: DB,
):
    await paytrail_callback.to_payment_stamp(
        event,
        order,
        PaymentStampType.PAYMENT_REDIRECT,
    ).save(db)

    return RedirectResponse(order.get_url(event.slug), 303)


@app.get("/api/tickets-v2/{event_slug}/orders/{order_id}/callback/")
async def paytrail_callback(
    event: _Event,
    order: _Order,
    paytrail_callback: _Callback,
    db: DB,
):
    await paytrail_callback.to_payment_stamp(
        event,
        order,
        PaymentStampType.PAYMENT_CALLBACK,
    ).save(db)

    return PlainTextResponse("")
