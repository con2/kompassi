from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, HTTPException, Path

from .db import DB, lifespan
from .excs import InvalidProducts, NotEnoughTickets
from .models.event import Event
from .models.order import CreateOrderRequest, Order
from .models.product import Product

app = FastAPI(lifespan=lifespan)


EventSlug = Annotated[str, Path()]


@app.get("/api/tickets-v2/status/")
async def status():
    return {"status": "OK"}


@app.get("/api/tickets-v2/{event_slug}/products/")
async def get_products(event_slug: EventSlug, db: DB):
    event = await Event.get_event_by_slug(db, event_slug)
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
    event = await Event.get_event_by_slug(db, event_slug)
    if event is None:
        raise HTTPException(status_code=400, detail="INVALID_ORDER")

    try:
        async with db.transaction():
            order_id = await order.save(db, event.id)
    except NotEnoughTickets as e:
        raise HTTPException(409, "NOT_ENOUGH_TICKETS") from e
    except InvalidProducts as e:
        raise HTTPException(400, "INVALID_ORDER") from e

    # TODO empaymenten

    return {
        "orderId": order_id,
        # payment_redirect=response["href"],
        "paymentRedirect": "",
    }


@app.get("/api/tickets-v2/{event_slug}/orders/{order_id}/")
async def get_order(event_slug: EventSlug, order_id: UUID, db: DB):
    event = await Event.get_event_by_slug(db, event_slug)
    if event is None:
        raise HTTPException(status_code=400, detail="EVENT_NOT_FOUND")

    order = await Order.get_order(db, event.id, order_id)
    if order is None:
        raise HTTPException(status_code=400, detail="ORDER_NOT_FOUND")

    return {
        "event": {
            "name": event.name,
        },
        "order": order.model_dump(),
    }
