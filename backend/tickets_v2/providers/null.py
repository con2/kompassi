from dataclasses import dataclass

from core.models.event import Event

from ..models.payment_stamp import PaymentStamp


@dataclass
class NullProvider:
    event: Event

    def prepare_refund(self, payment_stamp: PaymentStamp):
        raise NotImplementedError("The null provider does not support refunds")
