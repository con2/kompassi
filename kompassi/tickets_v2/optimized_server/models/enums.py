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

    @functools.cached_property
    def _ordinal(self) -> int:
        # Enum members are singletons, so this is computed once per member. Doing the
        # lookup per comparison instead would rebuild the member list every time.
        return self._member_names_.index(self._name_)

    def __lt__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self._ordinal < other._ordinal


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

    def to_receipt_type(self) -> ReceiptType:
        """
        The kind of receipt an order in this status is owed, or ValueError if it is owed
        none. This is the single authority on that question: callers should not pre-screen
        with their own status comparison, because ordering does not decide it (both the
        unpaid statuses below PAID and PAID_AFTER_CANCELLATION above it get no receipt).
        """
        match self:
            case PaymentStatus.PAID:
                return ReceiptType.PAID
            case PaymentStatus.CANCELLED:
                return ReceiptType.CANCELLED
            case PaymentStatus.REFUND_REQUESTED | PaymentStatus.REFUND_FAILED | PaymentStatus.REFUNDED:
                return ReceiptType.REFUNDED
            case PaymentStatus.NOT_STARTED | PaymentStatus.PENDING | PaymentStatus.FAILED:
                raise ValueError("No receipt for unpaid orders")
            case PaymentStatus.PAID_AFTER_CANCELLATION:
                # Paid, but holding no tickets: a receipt here would email an e-ticket
                # PDF for an order that owns nothing. Resolved by fulfilling (-> PAID)
                # or refunding (-> REFUNDED), each of which does produce a receipt.
                raise ValueError("No receipt for an order paid after cancellation")
            case _:
                raise ValueError(f"No receipt for an order in status {self.name}")

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
