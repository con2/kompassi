from ..models.payment_stamp import PaymentStamp


class NullProvider:
    def prepare_refund(self, _payment_stamp: PaymentStamp):
        raise NotImplementedError("The null provider does not support refunds")


NULL_PROVIDER = NullProvider()
