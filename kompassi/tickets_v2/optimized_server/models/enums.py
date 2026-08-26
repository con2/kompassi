from __future__ import annotations

import functools
from enum import Enum


@functools.total_ordering
class OrderedEnum(Enum):
    """
    Comparison follows declaration order, mirroring the PostgreSQL enum types these are
    stored as. Declaration order is therefore load-bearing and must match the label order
    of the corresponding type; test_enum_declaration_order_matches_database guards it.
    """

    def __lt__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        members = list(self.__class__)
        return members.index(self) < members.index(other)


class PaymentProvider(OrderedEnum):
    NONE = "NONE"
    PAYTRAIL = "PAYTRAIL"
    STRIPE = "STRIPE"


class PaymentStampType(OrderedEnum):
    ZERO_PRICE = "ZERO_PRICE"

    CREATE_PAYMENT_REQUEST = "CREATE_PAYMENT_REQUEST"
    CREATE_PAYMENT_SUCCESS = "CREATE_PAYMENT_SUCCESS"
    CREATE_PAYMENT_FAILURE = "CREATE_PAYMENT_FAILURE"

    PAYMENT_REDIRECT = "PAYMENT_REDIRECT"
    PAYMENT_CALLBACK = "PAYMENT_CALLBACK"

    CANCEL_WITHOUT_REFUND = "CANCEL_WITHOUT_REFUND"

    CREATE_REFUND_REQUEST = "CREATE_REFUND_REQUEST"
    CREATE_REFUND_SUCCESS = "CREATE_REFUND_SUCCESS"
    CREATE_REFUND_FAILURE = "CREATE_REFUND_FAILURE"

    REFUND_CALLBACK = "REFUND_CALLBACK"
    MANUAL_REFUND = "MANUAL_REFUND"
    MANUAL_FULFILMENT = "MANUAL_FULFILMENT"


class PaymentStatus(OrderedEnum):
    NOT_STARTED = "NOT_STARTED"
    PENDING = "PENDING"
    FAILED = "FAILED"
    PAID = "PAID"

    CANCELLED = "CANCELLED"
    PAID_AFTER_CANCELLATION = "PAID_AFTER_CANCELLATION"

    REFUND_REQUESTED = "REFUND_REQUESTED"
    REFUND_FAILED = "REFUND_FAILED"
    REFUNDED = "REFUNDED"

    def to_receipt_type(self):
        match self:
            case PaymentStatus.NOT_STARTED | PaymentStatus.PENDING | PaymentStatus.FAILED:
                raise ValueError("No receipt for unpaid orders")
            case PaymentStatus.PAID:
                return ReceiptType.PAID
            case PaymentStatus.CANCELLED:
                return ReceiptType.CANCELLED
            case PaymentStatus.REFUND_REQUESTED | PaymentStatus.REFUND_FAILED | PaymentStatus.REFUNDED:
                return ReceiptType.REFUNDED
            case _:
                raise NotImplementedError(f"Unsupported status: {self}")

    @property
    def is_refundable(self):
        match self:
            case (
                PaymentStatus.PAID
                | PaymentStatus.CANCELLED
                | PaymentStatus.REFUND_FAILED
                | PaymentStatus.PAID_AFTER_CANCELLATION
            ):
                return True
            case _:
                return False

    @property
    def is_payable(self):
        match self:
            case PaymentStatus.NOT_STARTED | PaymentStatus.PENDING | PaymentStatus.FAILED:
                return True
            case _:
                return False

    @property
    def is_owner_cancelable(self):
        match self:
            case PaymentStatus.NOT_STARTED | PaymentStatus.PENDING | PaymentStatus.FAILED:
                return True
            case _:
                return False

    @property
    def is_fulfillable(self):
        return self.is_payable or self is PaymentStatus.PAID_AFTER_CANCELLATION


class ReceiptType(OrderedEnum):
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class ReceiptStatus(OrderedEnum):
    REQUESTED = "REQUESTED"
    PROCESSING = "PROCESSING"
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"

    # could add:
    # BOUNCE = 4


class RefundType(Enum):
    NONE = "NONE"
    MANUAL = "MANUAL"
    PROVIDER = "PROVIDER"

    @property
    def event_log_entry_type(self):
        match self:
            case RefundType.NONE:
                return "tickets_v2.order.cancelled"
            case RefundType.MANUAL:
                return "tickets_v2.order.refunded.manual"
            case RefundType.PROVIDER:
                return "tickets_v2.order.refunded.provider"
            case _:
                raise NotImplementedError(f"Unsupported refund type: {self}")
