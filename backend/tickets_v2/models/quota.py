from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import models, transaction

from core.models.event import Event
from tickets_v2.optimized_server.utils.uuid7 import uuid7

if TYPE_CHECKING:
    from .product import Product

batch_size = 400
logger = logging.getLogger("kompassi")


class Quota(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="quotas",
    )
    name = models.TextField()

    id: int
    pk: int
    products: models.QuerySet[Product]

    def __str__(self):
        return f"{self.event}: {self.name}"

    @property
    def tickets(self):
        from .ticket import Ticket

        return Ticket.objects.filter(event=self.event, quota=self)

    @property
    def is_available(self):
        return self.tickets.filter(order_id__isnull=True).exists()

    def set_quota(self, quota: int):
        with transaction.atomic():
            num_current_tickets = self.tickets.count()
            adjustment = quota - num_current_tickets

            if adjustment < 0:
                self.delete_tickets(-adjustment)
            elif adjustment > 0:
                self.create_tickets(adjustment)

    def delete_tickets(self, num_tickets_to_delete: int):
        logger.info(f"Deleting {num_tickets_to_delete} tickets from {self}")
        tickets_to_delete = self.tickets.filter(order_id__isnull=True).select_for_update()[:num_tickets_to_delete]
        _, deleted_by_model = tickets_to_delete.delete()
        num_tickets_deleted = deleted_by_model.get("tickets_v2.Ticket", 0)
        if num_tickets_deleted != num_tickets_to_delete:
            raise ValueError(
                f"Expected to delete {num_tickets_to_delete} tickets, "
                f"but was only able to delete {num_tickets_deleted}"
            )

    def create_tickets(self, num_tickets: int):
        from .ticket import Ticket

        logger.info(f"Creating {num_tickets} tickets for {self}")

        Ticket.objects.bulk_create(
            (
                Ticket(
                    id=uuid7(),
                    event=self.event,
                    quota=self,
                )
                for _ in range(num_tickets)
            ),
            batch_size=batch_size,
        )
