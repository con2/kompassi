from uuid import UUID

import pydantic

from .product import Product


class LimitedEvent(pydantic.BaseModel):
    name: str


class GetProductsResponse(pydantic.BaseModel):
    event: LimitedEvent
    products: list[Product]


class CreateOrderResponse(pydantic.BaseModel):
    order_id: UUID
    payment_redirect: str
