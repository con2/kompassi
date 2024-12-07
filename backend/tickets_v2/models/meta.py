from django.db import models

from core.models.event_meta_base import EventMetaBase

from ..optimized_server.models.enums import PaymentProvider


class TicketsV2EventMeta(EventMetaBase):
    provider = models.SmallIntegerField(
        choices=[(x.value, x.name) for x in PaymentProvider],
        default=PaymentProvider.NONE,
    )

    def ensure_partitions(self):
        from .order import Order
        from .payment_stamp import PaymentStamp
        from .ticket import Ticket

        Order.ensure_partition(self.event)
        Ticket.ensure_partition(self.event)
        PaymentStamp.ensure_partition(self.event)
