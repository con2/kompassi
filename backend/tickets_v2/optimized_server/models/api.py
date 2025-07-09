from uuid import UUID

import pydantic

from .enums import PaymentStatus
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
    status: PaymentStatus

    @pydantic.field_validator("status", mode="before")
    @staticmethod
    def validate_status(value: str | int | PaymentStatus):
        if isinstance(value, str):
            return PaymentStatus[value]
        else:
            return PaymentStatus(value)


class GetOrderResponse(pydantic.BaseModel):
    event: LimitedEvent
    order: Order
