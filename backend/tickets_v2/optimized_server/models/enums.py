from enum import IntEnum


class PaymentProvider(IntEnum):
    NONE = 0
    PAYTRAIL = 1
    STRIPE = 2


class PaymentStampType(IntEnum):
    ZERO_PRICE = 0

    CREATE_PAYMENT_REQUEST = 1
    CREATE_PAYMENT_SUCCESS = 2
    CREATE_PAYMENT_FAILURE = 3

    PAYMENT_REDIRECT = 4
    PAYMENT_CALLBACK = 5


class PaymentStatus(IntEnum):
    NOT_STARTED = 0
    PENDING = 1
    FAILED = 2
    PAID = 3
    CANCELLED = 4
    REFUNDED = 5


class ReceiptType(IntEnum):
    ORDER_CONFIRMATION = 1
    CANCELLATION = 2


class ReceiptStatus(IntEnum):
    REQUESTED = 0
    PROCESSING = 1
    FAILURE = 2
    SUCCESS = 3

    # could add:
    # BOUNCE = 4
