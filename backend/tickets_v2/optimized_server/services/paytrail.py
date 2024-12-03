from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from datetime import date as date_type
from typing import Literal
from uuid import UUID, uuid4

import aiohttp
import pydantic
from psycopg import AsyncConnection

from tickets_v2.optimized_server.utils.uuid7 import uuid7

from ..config import TICKETS_BASE_URL
from ..models.customer import Customer
from ..models.enums import PaymentProvider, PaymentStampType, PaymentStatus
from ..models.event import Event
from ..models.order import CreateOrderRequest, CreateOrderResult, OrderWithCustomer
from ..models.payment_stamp import PaymentStamp
from ..utils.paytrail_hmac import calculate_hmac

PAYTRAIL_API_URL = "https://services.paytrail.com/payments"
logger = logging.getLogger(__name__)


def get_params(event: Event, method="POST", t=None):
    if event.provider != PaymentProvider.PAYTRAIL:
        raise ValueError(f"Event {event.slug} is not using Paytrail")

    if t is None:
        t = datetime.now(UTC)

    return {
        "checkout-account": event.paytrail_merchant,
        "checkout-algorithm": "sha256",
        "checkout-method": method,
        "checkout-nonce": str(uuid4()),
        "checkout-timestamp": t.isoformat(),
    }


class Item(pydantic.BaseModel):
    unit_price_cents: int = pydantic.Field(serialization_alias="unitPrice")
    units: int
    vat_percentage: Literal[0] = pydantic.Field(serialization_alias="vatPercentage", default=0)
    product_code: str = pydantic.Field(serialization_alias="productCode")
    delivery_date: date_type = pydantic.Field(serialization_alias="deliveryDate")
    description: str | None = None


class CallbackUrls(pydantic.BaseModel):
    success: str
    failure: str

    @classmethod
    def get_redirect_urls_for_order_id(cls, event_slug: str, order_id: UUID) -> CallbackUrls:
        return cls(
            success=f"{TICKETS_BASE_URL}/api/tickets-v2/{event_slug}/orders/{order_id}/redirect-success/",
            failure=f"{TICKETS_BASE_URL}/api/tickets-v2/{event_slug}/orders/{order_id}/redirect-failure/",
        )

    @classmethod
    def get_callback_urls_for_order_id(cls, event_slug: str, order_id: UUID) -> CallbackUrls:
        return cls(
            success=f"{TICKETS_BASE_URL}/api/tickets-v2/{event_slug}/orders/{order_id}/callback-success/",
            failure=f"{TICKETS_BASE_URL}/api/tickets-v2/{event_slug}/orders/{order_id}/callback-failure/",
        )


class CreatePaymentResponse(pydantic.BaseModel):
    transaction_id: str = pydantic.Field(validation_alias="transactionId")
    href: str
    reference: str


class CreatePaymentRequest(pydantic.BaseModel):
    """
    Docs: https://docs.paytrail.com/#/
    Examples: https://docs.paytrail.com/#/examples?id=create
    """

    stamp: UUID = pydantic.Field(default_factory=uuid7)
    reference: str
    amount_cents: int = pydantic.Field(serialization_alias="amount")
    currency: Literal["EUR"] = "EUR"
    language: str
    customer: Customer
    redirect_urls: CallbackUrls = pydantic.Field(serialization_alias="redirectUrls")
    callback_urls: CallbackUrls | None = pydantic.Field(serialization_alias="callbackUrls")

    @classmethod
    def from_create_order_request(
        cls,
        event: Event,
        request: CreateOrderRequest,
        result: CreateOrderResult,
    ) -> CreatePaymentRequest:
        return cls(
            reference=result.reference,
            amount_cents=int(result.total_price * 100),
            language=request.language.upper(),
            customer=request.customer,
            redirect_urls=CallbackUrls.get_redirect_urls_for_order_id(event.slug, result.order_id),
            callback_urls=(
                CallbackUrls.get_callback_urls_for_order_id(event.slug, result.order_id)
                if "localhost" not in TICKETS_BASE_URL
                else None
            ),
        )

    @classmethod
    def from_order(
        cls,
        event: Event,
        order: OrderWithCustomer,
        language: str,
    ) -> CreatePaymentRequest:
        return cls(
            reference=order.reference,
            amount_cents=int(order.total_price * 100),
            language=language.upper(),
            customer=order.customer,
            redirect_urls=CallbackUrls.get_redirect_urls_for_order_id(event.slug, order.id),
            callback_urls=(
                CallbackUrls.get_callback_urls_for_order_id(event.slug, order.id)
                if "localhost" not in TICKETS_BASE_URL
                else None
            ),
        )

    async def send(
        self,
        db: AsyncConnection,
        event: Event,
        order_id: UUID,
        url: str = PAYTRAIL_API_URL,
    ):
        data = self.model_dump(mode="json", by_alias=True, exclude_none=True)
        body = json.dumps(data)
        headers = get_params(event, method="POST")
        headers["signature"] = calculate_hmac(event.paytrail_password, headers, body)
        headers["content-type"] = "application/json"

        # sensitive and uninteresting fields not to be stored in payment stamp
        del data["customer"]
        del data["redirectUrls"]
        if "callbackUrls" in data:
            del data["callbackUrls"]

        # TODO fire and forget?
        # TODO do simultaneously with sending the request?
        await PaymentStamp(
            event_id=event.id,
            order_id=order_id,
            provider=PaymentProvider.PAYTRAIL,
            type=PaymentStampType.CREATE_PAYMENT_REQUEST,
            status=PaymentStatus.PENDING,
            correlation_id=self.stamp,
            data=data,
        ).save(db)

        # TODO connection pool?
        async with aiohttp.ClientSession() as session, session.post(url, data=body, headers=headers) as response:
            try:
                response.raise_for_status()
            except aiohttp.ClientResponseError:
                logger.error("Error response from Paytrail:\n%s", await response.text())
                raise
            data = await response.json()

        result = CreatePaymentResponse.model_validate(data)

        await PaymentStamp(
            event_id=event.id,
            order_id=order_id,
            provider=PaymentProvider.PAYTRAIL,
            type=PaymentStampType.CREATE_PAYMENT_RESPONSE,
            status=PaymentStatus.PENDING,
            correlation_id=self.stamp,
            data=data,
        ).save(db)

        return result
