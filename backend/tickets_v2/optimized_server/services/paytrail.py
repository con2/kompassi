from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from datetime import UTC, datetime
from enum import Enum
from typing import Literal, Self
from uuid import UUID, uuid4

import aiohttp
import pydantic
from fastapi import HTTPException

from tickets_v2.optimized_server.utils.uuid7 import uuid7

from ..config import TICKETS_BASE_URL
from ..models.customer import Customer
from ..models.enums import PaymentProvider, PaymentStampType, PaymentStatus
from ..models.event import Event
from ..models.order import CreateOrderRequest, CreateOrderResult, Order, OrderWithCustomer
from ..models.payment_stamp import PaymentStamp
from ..utils.paytrail_hmac import calculate_hmac

PAYTRAIL_API_URL = "https://services.paytrail.com/payments"
# PAYTRAIL_API_URL = "https://api.checkout.fi/payments"
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
        "checkout-timestamp": t.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "platform-name": "kompassi",
    }


class Item(pydantic.BaseModel):
    unit_price_cents: int = pydantic.Field(serialization_alias="unitPrice")
    units: int
    vat_percentage: Literal[0] = pydantic.Field(serialization_alias="vatPercentage", default=0)
    product_code: str = pydantic.Field(serialization_alias="productCode")


class CallbackUrls(pydantic.BaseModel):
    success: str
    cancel: str

    @classmethod
    def get_redirect_urls_for_order_id(cls, event_slug: str, order_id: UUID) -> CallbackUrls:
        url = f"{TICKETS_BASE_URL}/api/tickets-v2/{event_slug}/orders/{order_id}/redirect/"
        return cls(
            success=url,
            cancel=url,
        )

    @classmethod
    def get_callback_urls_for_order_id(cls, event_slug: str, order_id: UUID) -> CallbackUrls:
        url = f"{TICKETS_BASE_URL}/api/tickets-v2/{event_slug}/orders/{order_id}/callback/"
        return cls(
            success=url,
            cancel=url,
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
    items: list[Item]
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
            items=[
                Item(
                    unit_price_cents=int(result.total_price * 100),
                    units=1,
                    product_code=str(result.order_id),
                )
            ],
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
            items=[
                Item(
                    unit_price_cents=int(order.total_price * 100),
                    units=1,
                    product_code=str(order.id),
                )
            ],
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
        event: Event,
        order_id: UUID,
        url: str = PAYTRAIL_API_URL,
    ) -> tuple[CreatePaymentResponse, list[PaymentStamp]]:
        stamps = []
        data = self.model_dump(mode="json", by_alias=True, exclude_none=True)
        body = json.dumps(data)
        headers = get_params(event, method="POST")
        headers["signature"] = calculate_hmac(event.paytrail_password, headers, body)
        headers["content-type"] = "application/json; charset=utf-8"

        # sensitive and uninteresting fields not to be stored in payment stamp
        del data["customer"]
        del data["redirectUrls"]
        if "callbackUrls" in data:
            del data["callbackUrls"]

        stamps.append(
            PaymentStamp(
                event_id=event.id,
                order_id=order_id,
                provider=PaymentProvider.PAYTRAIL,
                type=PaymentStampType.CREATE_PAYMENT_REQUEST,
                status=PaymentStatus.PENDING,
                correlation_id=self.stamp,
                data=data,
            )
        )

        # TODO connection pool?
        # TODO if there is an error with Paytrail, should we still save the stamps?
        async with aiohttp.ClientSession() as session, session.post(url, data=body, headers=headers) as response:
            try:
                response.raise_for_status()
            except aiohttp.ClientResponseError:
                logger.error("Error response from Paytrail:\n%s", await response.text())
                raise
                # TODO save error in payment stamp and _commit the transaction_?
                # now if we error here, payment stamp won't get recorded
            data = await response.json()

        result = CreatePaymentResponse.model_validate(data)

        stamps.append(
            PaymentStamp(
                event_id=event.id,
                order_id=order_id,
                provider=PaymentProvider.PAYTRAIL,
                type=PaymentStampType.CREATE_PAYMENT_RESPONSE,
                status=PaymentStatus.PENDING,
                correlation_id=self.stamp,
                # use parsed version because response is huge
                data=result.model_dump(mode="json", by_alias=True),
            )
        )

        return result, stamps


class PaytrailStatus(str, Enum):
    OK = "ok"
    PENDING = "pending"
    DELAYED = "delayed"
    FAIL = "fail"

    def to_payment_status(self):
        match self:
            case PaytrailStatus.OK:
                return PaymentStatus.PAID
            case PaytrailStatus.PENDING:
                return PaymentStatus.PENDING
            case PaytrailStatus.DELAYED:
                # TODO do we need to add this to PaymentStatus?
                return PaymentStatus.PENDING
            case PaytrailStatus.FAIL:
                return PaymentStatus.PENDING


class PaymentCallback(pydantic.BaseModel, populate_by_name=True):
    account: str = pydantic.Field(
        serialization_alias="checkout-account",
        validation_alias="checkout-account",
    )

    algorithm: str = pydantic.Field(
        serialization_alias="checkout-algorithm",
        validation_alias="checkout-algorithm",
    )

    amount_cents: int = pydantic.Field(
        serialization_alias="checkout-amount",
        validation_alias="checkout-amount",
    )

    stamp: UUID = pydantic.Field(
        serialization_alias="checkout-stamp",
        validation_alias="checkout-stamp",
    )

    reference: str = pydantic.Field(
        serialization_alias="checkout-reference",
        validation_alias="checkout-reference",
    )

    transaction_id: str = pydantic.Field(
        serialization_alias="checkout-transaction-id",
        validation_alias="checkout-transaction-id",
    )

    status: PaytrailStatus = pydantic.Field(
        serialization_alias="checkout-status",
        validation_alias="checkout-status",
    )

    provider: str = pydantic.Field(
        serialization_alias="checkout-provider",
        validation_alias="checkout-provider",
    )

    signature: str = pydantic.Field(
        serialization_alias="signature",
        validation_alias="signature",
    )

    @classmethod
    def from_query_params(cls, query_params: Mapping[str, str], event: Event) -> Self:
        provided_signature = query_params["signature"]
        calculated_signature = calculate_hmac(
            secret=event.paytrail_password,
            params=query_params,
            body="",
        )

        if provided_signature != calculated_signature:
            raise HTTPException(status_code=401, detail="SIGNATURE_MISMATCH")

        return cls.model_validate(query_params)

    def to_payment_stamp(
        self,
        event: Event,
        order: Order,
        type: Literal[PaymentStampType.PAYMENT_REDIRECT, PaymentStampType.PAYMENT_CALLBACK],
    ):
        if event.paytrail_merchant != self.account:
            raise HTTPException(status_code=400, detail="ACCOUNT_MISMATCH")

        return PaymentStamp(
            event_id=event.id,
            order_id=order.id,
            provider=PaymentProvider.PAYTRAIL,
            type=type,
            status=self.status.to_payment_status(),
            correlation_id=self.stamp,
            data=self.model_dump(mode="json", by_alias=True),
        )
