from dataclasses import dataclass

from django.db import models

from core.models.event_meta_base import EventMetaBase
from core.models.person import Person

from ..optimized_server.models.enums import PaymentProvider


class TicketsV2EventMeta(EventMetaBase):
    provider = models.SmallIntegerField(
        choices=[(x.value, x.name) for x in PaymentProvider],
        default=PaymentProvider.NONE,
    )

    def ensure_partitions(self):
        from .order import Order, OrderOwner
        from .payment_stamp import PaymentStamp
        from .receipts import ReceiptStamp
        from .ticket import Ticket

        Order.ensure_partition(self.event)
        OrderOwner.ensure_partition(self.event)
        Ticket.ensure_partition(self.event)
        PaymentStamp.ensure_partition(self.event)
        ReceiptStamp.ensure_partition(self.event)


@dataclass
class TicketsV2ProfileMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    person: Person
