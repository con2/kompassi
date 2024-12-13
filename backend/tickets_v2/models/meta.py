from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.db import models

from core.models.event_meta_base import EventMetaBase
from core.models.person import Person

from ..optimized_server.models.enums import PaymentProvider

if TYPE_CHECKING:
    pass


class TicketsV2EventMeta(EventMetaBase):
    provider_id = models.SmallIntegerField(
        choices=[(x.value, x.name) for x in PaymentProvider],
        default=PaymentProvider.NONE,
    )

    use_cbac = True

    def ensure_partitions(self):
        from .order import Order, OrderOwner
        from .payment_stamp import PaymentStamp
        from .receipt import Receipt
        from .ticket import Ticket

        Order.ensure_partition(self.event)
        OrderOwner.ensure_partition(self.event)
        Ticket.ensure_partition(self.event)
        PaymentStamp.ensure_partition(self.event)
        Receipt.ensure_partition(self.event)

    @property
    def scope(self):
        return self.event.scope


@dataclass
class TicketsV2ProfileMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    person: Person
