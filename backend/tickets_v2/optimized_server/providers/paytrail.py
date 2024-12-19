from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import Any, ClassVar, Literal, Self
from uuid import UUID, uuid4

import aiohttp
import pydantic
from fastapi import HTTPException

from tickets_v2.optimized_server.utils.uuid7 import uuid7

from ..config import TICKETS_BASE_URL
from ..excs import ProviderCannot
from ..models.customer import Customer
from ..models.enums import PaymentProvider, PaymentStampType, PaymentStatus
from ..models.event import Event
from ..models.order import CreateOrderRequest, CreateOrderResult, Order, OrderWithCustomer
from ..models.payment_stamp import PaymentStamp
from ..utils.paytrail_hmac import calculate_hmac

PAYTRAIL_API_URL = "https://services.paytrail.com/payments"
# PAYTRAIL_API_URL = "https://api.checkout.fi/payments"
logger = logging.getLogger(__name__)


def get_params(paytrail_merchant: str, method="POST", t=None):
    if t is None:
        t = datetime.now(UTC)

    return {
        "checkout-account": paytrail_merchant,
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
    def get_redirects_for_order(cls, event_slug: str, order_id: UUID) -> CallbackUrls:
        url = f"{TICKETS_BASE_URL}/api/tickets-v2/{event_slug}/orders/{order_id}/redirect/"
        return cls(
            success=url,
            cancel=url,
        )

    @classmethod
    def get_callbacks_for_order(cls, event_slug: str, order_id: UUID) -> CallbackUrls | None:
        if "localhost" in TICKETS_BASE_URL:
            return None

        url = f"{TICKETS_BASE_URL}/api/tickets-v2/{event_slug}/orders/{order_id}/callback/"
        return cls(
            success=url,
            cancel=url,
        )


class CreatePaymentResponse(pydantic.BaseModel):
    transaction_id: str = pydantic.Field(
        validation_alias="transactionId",
        serialization_alias="transactionId",
    )
    payment_redirect: str = pydantic.Field(
        validation_alias="href",
        serialization_alias="href",
    )
    reference: str


class CreatePaymentRequest(pydantic.BaseModel):
    """
    Represents the body of a valid Create Payment Request for Paytrail.

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
            redirect_urls=CallbackUrls.get_redirects_for_order(event.slug, result.order_id),
            callback_urls=CallbackUrls.get_callbacks_for_order(event.slug, result.order_id),
        )

    @classmethod
    def from_order(
        cls,
        event: Event,
        order: OrderWithCustomer,
    ) -> CreatePaymentRequest:
        return cls(
            reference=order.reference,
            amount_cents=int(order.total_price * 100),
            language=order.language.upper(),
            customer=order.customer,
            redirect_urls=CallbackUrls.get_redirects_for_order(event.slug, order.id),
            callback_urls=CallbackUrls.get_callbacks_for_order(event.slug, order.id),
        )

    def prepare(
        self,
        event: Event,
        order_id: UUID,
    ) -> tuple[PreparedCreatePaymentRequest, PaymentStamp]:
        data = self.model_dump(mode="json", by_alias=True, exclude_none=True)
        body = json.dumps(data)
        headers = get_params(event.paytrail_merchant, method="POST")
        headers["signature"] = calculate_hmac(event.paytrail_password, headers, body)
        headers["content-type"] = "application/json; charset=utf-8"

        # sensitive and uninteresting fields not to be stored in payment stamp
        del data["customer"]
        # del data["redirectUrls"]
        # if "callbackUrls" in data:
        #     del data["callbackUrls"]

        request_stamp = PaymentStamp(
            event_id=event.id,
            order_id=order_id,
            provider_id=PaymentProvider.PAYTRAIL,
            type=PaymentStampType.CREATE_PAYMENT_REQUEST,
            status=PaymentStatus.PENDING,
            correlation_id=self.stamp,
            data=data,
        )

        return PreparedCreatePaymentRequest(
            body=body,
            headers=headers,
            request_stamp=request_stamp,
        ), request_stamp


class PreparedCreatePaymentRequest(pydantic.BaseModel):
    """
    The Create Payment Request is performed in three parts:

    1. In same transaction as the order creation:
        - Instantiate a CreatePaymentRequest
        - Call .prepare() on it
        - Store the .payment_stamp in the database
    2. Outside transaction (important!)
        - Call .send() on the PreparedCreatePaymentRequest
    3. In another transaction
        - Store the .payment_stamp of the CreatePaymentResult in the database

    This ensures we get the payment stamp stored even if the payment fails,
    minimizes amount of waiting inside transaction and
    and minimizes number of transactions involved.
    """

    body: str
    headers: dict[str, str]
    request_stamp: PaymentStamp

    def _build_response_stamp(
        self,
        type: PaymentStampType,
        data: dict[str, Any],
    ):
        return PaymentStamp(
            event_id=self.request_stamp.event_id,
            order_id=self.request_stamp.order_id,
            provider_id=PaymentProvider.PAYTRAIL,
            type=type,
            status=PaymentStatus.PENDING,
            correlation_id=self.request_stamp.correlation_id,
            data=data,
        )

    async def send(
        self,
        url: str = PAYTRAIL_API_URL,
    ) -> tuple[CreatePaymentResponse | None, PaymentStamp]:
        async with (
            aiohttp.ClientSession() as session,
            session.post(
                url,
                data=self.body,
                headers=self.headers,
            ) as response,
        ):
            try:
                response.raise_for_status()
            except aiohttp.ClientResponseError:
                error = await response.text()
                logger.error("Error response from Paytrail:\n%s", error)

                try:
                    error = json.loads(error)
                except json.JSONDecodeError:
                    pass

                return None, self._build_response_stamp(
                    PaymentStampType.CREATE_PAYMENT_FAILURE,
                    data={"error": error},
                )

            data = await response.json()

        result = CreatePaymentResponse.model_validate(data)
        stamp = self._build_response_stamp(
            PaymentStampType.CREATE_PAYMENT_SUCCESS,
            # use parsed version to strip uninteresting fields (whole result is huge)
            data=result.model_dump(mode="json", by_alias=True),
        )

        return result, stamp


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
                # user cancelled or payment failed
                return PaymentStatus.FAILED


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

    provider_name: str = pydantic.Field(
        serialization_alias="checkout-provider",
        validation_alias="checkout-provider",
        description="Paytrail sub-provider name, eg. 'op', 'mobilepay', 'creditcard' etc.",
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
            provider_id=PaymentProvider.PAYTRAIL,
            type=type,
            status=self.status.to_payment_status(),
            correlation_id=self.stamp,
            data=self.model_dump(mode="json", by_alias=True),
        )


@dataclass
class PaytrailProvider:
    """
    Implements creating payments for Paytrail.

    Note that refunds are implemented on the Django side.
    """

    event: Event

    provider_id: ClassVar[PaymentProvider] = PaymentProvider.PAYTRAIL

    def prepare_for_new_order(
        self,
        order: CreateOrderRequest,
        result: CreateOrderResult,
    ) -> tuple[PreparedCreatePaymentRequest | None, PaymentStamp]:
        if result.total_price == 0:
            return None, PaymentStamp.for_zero_price_order(
                self.event.id,
                result.order_id,
                self.provider_id,
            )
        elif result.total_price < 0:
            raise ProviderCannot("Paytrail provider cowardly refusing negative price order")

        return CreatePaymentRequest.from_create_order_request(
            self.event,
            order,
            result,
        ).prepare(
            self.event,
            result.order_id,
        )

    def prepare_for_existing_order(
        self,
        order: OrderWithCustomer,
    ) -> tuple[PreparedCreatePaymentRequest, PaymentStamp]:
        if order.total_price <= 0:
            raise ProviderCannot("Paytrail provider cowardly refusing existing nonpositive price order")

        return CreatePaymentRequest.from_order(
            self.event,
            order,
        ).prepare(
            self.event,
            order.id,
        )
