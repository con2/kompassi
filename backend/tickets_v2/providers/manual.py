from ..models.payment_stamp import PaymentStamp


class ManualProvider:
    def prepare_refund(self, _payment_stamp: PaymentStamp):
        raise NotImplementedError("The manual provider does not support refunds")


MANUAL_PROVIDER = ManualProvider()
