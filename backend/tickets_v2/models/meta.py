from core.models.event_meta_base import EventMetaBase


class TicketsV2EventMeta(EventMetaBase):
    def ensure_partitions(self):
        from .order import Order
        from .ticket import Ticket

        Order.ensure_partition(self.event)
        Ticket.ensure_partition(self.event)
