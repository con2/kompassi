from enum import IntEnum


class PaymentProvider(IntEnum):
    NONE = 0
    PAYTRAIL = 1
    STRIPE = 2


class PaymentStampType(IntEnum):
    CREATE_PAYMENT_REQUEST = 1
    CREATE_PAYMENT_RESPONSE = 2

    PAYMENT_REDIRECT = 3
    PAYMENT_CALLBACK = 4


class PaymentStatus(IntEnum):
    UNKNOWN = 0
    PENDING = 1
    PAID = 2
    REFUNDED = 3
