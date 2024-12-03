from __future__ import annotations

import logging
from functools import cached_property
from uuid import UUID

from django.db import models

from core.models.event import Event
from event_log_v2.utils.monthly_partitions import UUID7Mixin
from tickets_v2.optimized_server.utils.uuid7 import uuid7

from ..utils.event_partitions import EventPartitionsMixin
from .order import Order
from .quota import Quota

logger = logging.getLogger("kompassi")


class NotEnoughTickets(RuntimeError):
    pass


class UnsaneSituation(RuntimeError):
    pass


class Ticket(EventPartitionsMixin, UUID7Mixin, models.Model):
    """
    Partitioned by event_id.
    Primary key is (event_id, id).
    Migrations managed manually.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.RESTRICT,
        related_name="+",
    )
    quota = models.ForeignKey(
        Quota,
        on_delete=models.CASCADE,
        related_name="+",
    )
    order_id = models.UUIDField(
        null=True,
        blank=True,
    )

    event_id: int
    quota_id: int
    pk: UUID

    def __str__(self):
        return str(self.id)

    @cached_property
    def order(self):
        """
        Direct the query to the correct partition.
        """
        return Order.objects.get(event=self.event, id=self.order_id)
