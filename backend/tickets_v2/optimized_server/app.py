import logging
import os
from typing import Annotated, Literal
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Path, Query
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse

from graphql_api.language import DEFAULT_LANGUAGE, getattr_message_in_language

from .db import DB, lifespan
from .excs import InvalidProducts, NotEnoughTickets, ProviderCannot
from .models.enums import PaymentStampType
from .models.event import Event
from .models.order import CreateOrderRequest, Order, OrderWithCustomer
from .models.product import Product
from .providers.paytrail import PaymentCallback

app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)

EventSlug = Annotated[str, Path()]
OrderId = Annotated[UUID, Path()]

API_KEY = os.getenv("KOMPASSI_TICKETS_V2_API_KEY")


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


async def _api_key_verified(request: Request) -> Literal[True]:
    api_key = request.headers.get("x-api-key")
    if api_key is None or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    return True


_ApiKeyVerified = Annotated[Literal[True], Depends(_api_key_verified)]


@app.get("/api/tickets-v2/status/")
async def status():
    return {"status": "OK"}


_Language = Annotated[str, Query()]


@app.get("/api/tickets-v2/{event_slug}/products/")
async def get_products(
    event: _Event,
    db: DB,
    _api_key_verified: _ApiKeyVerified,
    language: _Language = DEFAULT_LANGUAGE,
):
    products = await Product.get_products(db, event.id)

    return {
        "event": {
            "name": event.name,
            "termsAndConditionsUrl": getattr_message_in_language(event, "terms_and_conditions_url", language),
        },
        "products": [product.model_dump(by_alias=True) for product in products],
    }


@app.post("/api/tickets-v2/{event_slug}/orders/")
async def create_order(
    event: _Event,
    order: CreateOrderRequest,
    db: DB,
    _api_key_verified: _ApiKeyVerified,
):
    provider = event.provider

    try:
        async with db.transaction():
            result = await order.save(db, event.id)
            request, request_stamp = provider.prepare_for_new_order(order, result)
            await request_stamp.save(db)
    except NotEnoughTickets as e:
        raise HTTPException(409, "NOT_ENOUGH_TICKETS") from e
    except (InvalidProducts, ProviderCannot) as e:
        raise HTTPException(400, "INVALID_ORDER") from e

    if request is None:
        return {
            "orderId": result.order_id,
            "status": request_stamp.status.name,
            "paymentRedirect": "",
        }

    response, response_stamp = await request.send()

    async with db.transaction():
        await response_stamp.save(db)

    return {
        "orderId": result.order_id,
        "status": response_stamp.status.name,
        "paymentRedirect": response.payment_redirect if response else "",
    }


@app.get("/api/tickets-v2/{event_slug}/orders/{order_id}/")
async def get_order(
    event: _Event,
    order: _Order,
    _api_key_verified: _ApiKeyVerified,
):
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
    db: DB,
    _api_key_verified: _ApiKeyVerified,
):
    provider = event.provider

    try:
        create_payment_request, request_stamp = provider.prepare_for_existing_order(order)
    except ProviderCannot as e:
        raise HTTPException(400, "INVALID_ORDER") from e

    async with db.transaction():
        await request_stamp.save(db)

    response, response_stamp = await create_payment_request.send()

    async with db.transaction():
        await response_stamp.save(db)

    return {
        "orderId": order.id,
        "status": response_stamp.status.name,
        "paymentRedirect": response.payment_redirect if response else "",
    }


def valid_callback(event: _Event, request: Request) -> PaymentCallback:
    return PaymentCallback.from_query_params(request.query_params, event)


_Callback = Annotated[PaymentCallback, Depends(valid_callback)]


# NOTE: The redirect view is accessed directly by the client browser, and the callback view is called by the provider.
# Therefore they do not require the API key.


@app.get("/api/tickets-v2/{event_slug}/orders/{order_id}/payment-redirect/")
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


@app.get("/api/tickets-v2/{event_slug}/orders/{order_id}/payment-callback/")
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


@app.get("/api/tickets-v2/{event_slug}/orders/{order_id}/refund-callback/")
async def paytrail_refund_callback(
    event: _Event,
    order: _Order,
    paytrail_callback: _Callback,
    db: DB,
):
    await paytrail_callback.to_payment_stamp(
        event,
        order,
        PaymentStampType.REFUND_CALLBACK,
    ).save(db)

    return PlainTextResponse("")
