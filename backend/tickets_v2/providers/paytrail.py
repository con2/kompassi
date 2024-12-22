import json
from dataclasses import dataclass
from uuid import UUID

import pydantic
import requests

from ..models.payment_stamp import PaymentStamp
from ..optimized_server.models.enums import PaymentProvider, PaymentStampType, PaymentStatus
from ..optimized_server.providers.paytrail import PAYTRAIL_API_URL, CallbackUrls, PaytrailStatus, get_params
from ..optimized_server.utils.paytrail_hmac import calculate_hmac
from ..optimized_server.utils.uuid7 import uuid7


class CreateRefundRequest(pydantic.BaseModel, populate_by_name=True):
    amount_cents: int = pydantic.Field(
        validation_alias="amount",
        serialization_alias="amount",
    )
    email: str
    refund_stamp: UUID = pydantic.Field(
        validation_alias="refundStamp",
        serialization_alias="refundStamp",
    )
    callback_urls: CallbackUrls = pydantic.Field(
        validation_alias="callbackUrls",
        serialization_alias="callbackUrls",
    )


class CreateRefundResponse(pydantic.BaseModel, populate_by_name=True):
    transaction_id: str = pydantic.Field(
        validation_alias="transactionId",
        serialization_alias="transactionId",
    )

    provider_name: str = pydantic.Field(
        validation_alias="provider",
        serialization_alias="provider",
    )

    status: PaytrailStatus


@dataclass
class PreparedCreateRefundRequest:
    url: str
    body: str
    headers: dict[str, str]
    request_stamp: PaymentStamp

    def _build_response_stamp(
        self,
        type: PaymentStampType,
        status: PaymentStatus,
        data: dict,
    ) -> PaymentStamp:
        return PaymentStamp(
            event=self.request_stamp.event,
            order_id=self.request_stamp.order_id,
            correlation_id=self.request_stamp.correlation_id,
            provider_id=PaymentProvider.PAYTRAIL,
            type=type,
            status=status,
            data=data,
        )

    def send(self) -> tuple[CreateRefundResponse | None, PaymentStamp]:
        response = requests.post(self.url, data=self.body, headers=self.headers)

        if response.status_code != 201:
            error = response.text
            try:
                error = json.loads(error)
            except json.JSONDecodeError:
                pass

            return None, self._build_response_stamp(
                type=PaymentStampType.CREATE_REFUND_FAILURE,
                status=PaymentStatus.REFUND_FAILED,
                data={"error": error},
            )

        result = CreateRefundResponse.model_validate(response.json())

        stamp = self._build_response_stamp(
            type=PaymentStampType.CREATE_REFUND_SUCCESS,
            status=PaymentStatus.REFUND_REQUESTED,
            data=result.model_dump(mode="json", by_alias=True),
        )

        return result, stamp


class PaytrailProvider:
    """
    Implements payment refunds for Paytrail.

    Note that creating payments is implemented on the optimized server (FastAPI) side.
    """

    def prepare_refund(self, payment_stamp: PaymentStamp) -> PreparedCreateRefundRequest:
        """
        Refund a payment.

        :param payment_stamp: The payment stamp to refund.
        """
        if payment_stamp.provider_id != PaymentProvider.PAYTRAIL:
            raise ValueError("Unsupported provider")
        if payment_stamp.status != PaymentStatus.PAID:
            raise ValueError("Payment must be in PAID status to refund")

        order = payment_stamp.order
        event = payment_stamp.event

        meta = event.tickets_v2_event_meta
        if meta is None:
            raise ValueError(f"Event {event} is not configured for Tickets v2")

        payments_meta = event.organization.payments_organization_meta
        if payments_meta is None:
            raise ValueError(f"Organization {event.organization} is not configured for payments")

        if payment_stamp.status != PaymentStatus.PAID:
            raise ValueError(
                "The payment stamp to refund must be a callback or redirect of a successful payment",
                payment_stamp,
            )

        payment_callback = payment_stamp.as_paytrail_payment_callback()

        paytrail_password = payments_meta.checkout_password
        paytrail_merchant = payments_meta.checkout_merchant
        transaction_id = payment_callback.transaction_id
        correlation_id = uuid7()

        callback_urls = CallbackUrls.for_refund_callback(order.event.slug, order.id)
        if callback_urls is None:
            raise ValueError("Cannot refund order without callback URLs")

        request = CreateRefundRequest(
            amount_cents=int(100 * order.cached_price),
            email=order.email,
            refund_stamp=correlation_id,
            callback_urls=callback_urls,
        )

        data = request.model_dump(mode="json", by_alias=True)
        body = json.dumps(data)
        headers = get_params(paytrail_merchant, method="POST")
        headers["checkout-transaction-id"] = transaction_id
        headers["signature"] = calculate_hmac(paytrail_password, headers, body)
        headers["content-type"] = "application/json; charset=utf-8"

        data.pop("callbackUrls")
        data["__transactionId"] = transaction_id

        url = f"{PAYTRAIL_API_URL}/{transaction_id}/refund"

        request_stamp = PaymentStamp(
            event=order.event,
            order_id=order.id,
            correlation_id=correlation_id,
            provider_id=PaymentProvider.PAYTRAIL,
            type=PaymentStampType.CREATE_REFUND_REQUEST,
            status=PaymentStatus.REFUND_REQUESTED,
            data=data,
        )

        return PreparedCreateRefundRequest(
            url=url,
            body=body,
            headers=headers,
            request_stamp=request_stamp,
        )


# singleton instance
PAYTRAIL_PROVIDER = PaytrailProvider()
