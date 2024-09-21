from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

from .db import DB, lifespan
from .excs import InvalidProducts, NotEnoughTickets
from .models.event import Event
from .models.order import Order
from .models.product import Product

app = FastAPI(lifespan=lifespan)


EventSlug = Annotated[str, Path()]


@app.get("/api/v1/status")
async def status():
    return {"status": "OK"}


@app.get("/api/tickets-v2/events/{event_slug}/products/")
async def get_products(event_slug: EventSlug, db: DB):
    event = await Event.get_event_by_slug(db, event_slug)
    if event is None:
        raise HTTPException(status_code=400, detail="event not found")

    products = await Product.get_products(db, event.id)

    return {
        "event": {
            "name": event.name,
        },
        "products": [product.model_dump() for product in products],
    }


@app.post("/api/tickets-v2/events/{event_slug}/orders/")
async def create_order(event_slug: EventSlug, order: Order, db: DB):
    event = await Event.get_event_by_slug(db, event_slug)
    if event is None:
        raise HTTPException(status_code=400, detail="event not found")

    try:
        async with db.transaction():
            order_id = await order.save(db, event.id)
    except NotEnoughTickets as e:
        raise HTTPException(409, "not enough tickets") from e
    except InvalidProducts as e:
        raise HTTPException(400, "invalid products") from e

    # TODO empaymenten

    return {
        "order_id": order_id,
        # payment_redirect=response["href"],
        "payment_redirect": "",
    }
