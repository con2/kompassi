from uuid import UUID

import pydantic

from .order import Order
from .product import Product


class LimitedEvent(pydantic.BaseModel):
    name: str


class GetProductsResponse(pydantic.BaseModel):
    event: LimitedEvent
    products: list[Product]


class CreateOrderResponse(pydantic.BaseModel, populate_by_name=True):
    order_id: UUID = pydantic.Field(alias="orderId")
    payment_redirect: str = pydantic.Field(alias="paymentRedirect", default="")


class GetOrderResponse(pydantic.BaseModel):
    event: LimitedEvent
    order: Order
