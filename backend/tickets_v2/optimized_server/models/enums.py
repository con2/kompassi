from enum import Enum, IntEnum


class PaymentProvider(IntEnum):
    NONE = 0
    PAYTRAIL = 1
    STRIPE = 2

    MANUAL = 9999


class PaymentStampType(IntEnum):
    ZERO_PRICE = 0

    CREATE_PAYMENT_REQUEST = 1
    CREATE_PAYMENT_SUCCESS = 2
    CREATE_PAYMENT_FAILURE = 3

    PAYMENT_REDIRECT = 4
    PAYMENT_CALLBACK = 5

    CANCEL_WITHOUT_REFUND = 6

    CREATE_REFUND_REQUEST = 7
    CREATE_REFUND_SUCCESS = 8
    CREATE_REFUND_FAILURE = 9

    REFUND_CALLBACK = 10
    MANUAL_REFUND = 11


class PaymentStatus(IntEnum):
    NOT_STARTED = 0
    PENDING = 1
    FAILED = 2
    PAID = 3

    CANCELLED = 4

    REFUND_REQUESTED = 5
    REFUND_FAILED = 6
    REFUNDED = 7

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
            case PaymentStatus.PAID | PaymentStatus.CANCELLED | PaymentStatus.REFUND_FAILED:
                return True
            case _:
                return False


class ReceiptType(IntEnum):
    PAID = PaymentStatus.PAID.value
    CANCELLED = PaymentStatus.CANCELLED.value
    REFUNDED = PaymentStatus.REFUNDED.value


class ReceiptStatus(IntEnum):
    REQUESTED = 0
    PROCESSING = 1
    FAILURE = 2
    SUCCESS = 3

    # could add:
    # BOUNCE = 4


class RefundType(str, Enum):
    NONE = "NONE"
    MANUAL = "MANUAL"
    PROVIDER = "PROVIDER"
