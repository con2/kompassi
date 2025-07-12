from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import pydantic
from django.conf import settings
from django.db import connection, models
from django.http import HttpRequest

from access.cbac import is_graphql_allowed_for_model
from core.models.event import Event
from tickets_v2.optimized_server.utils.uuid7 import uuid7

if TYPE_CHECKING:
    from .product import Product

batch_size = 400
logger = logging.getLogger("kompassi")


class QuotaCounters(pydantic.BaseModel):
    count_paid: int
    count_reserved: int
    count_available: int

    @pydantic.computed_field
    @property
    def count_total(self) -> int:
        return self.count_reserved + self.count_available

    query: ClassVar[str] = (Path(__file__).parent / "sql" / "get_quota_counters.sql").read_text()

    @staticmethod
    def get_for_event(event_id: int, request: HttpRequest | None) -> dict[int, QuotaCounters]:
        """
        Returns dict of quota_id -> (count_reserved, count_available) for the event.
        Cached per request.
        """
        # event_id -> product_id -> (count_reserved, count_available)
        cache: dict[int, dict[int, QuotaCounters]] | None = getattr(request, "_tickets_v2_quota_counters", None)
        if cache is None:
            cache = {}
            if request is not None:
                request._tickets_v2_quota_counters = cache  # type: ignore

        if event_cache := cache.get(event_id):
            return event_cache

        with connection.cursor() as cursor:
            cursor.execute(QuotaCounters.query, dict(event_id=event_id))
            counters = {
                quota_id: QuotaCounters(
                    count_paid=count_paid,
                    count_reserved=count_reserved,
                    count_available=count_available,
                )
                for quota_id, count_paid, count_reserved, count_available in cursor
            }

        cache[event_id] = counters
        return counters


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
    event_id: int

    def __str__(self):
        return f"{self.event}: {self.name}"

    @property
    def tickets(self):
        from .ticket import Ticket

        return Ticket.objects.filter(event=self.event, quota=self)

    @property
    def scope(self):
        return self.event.scope

    @property
    def admin_url(self):
        return f"{settings.KOMPASSI_V2_BASE_URL}/{self.event.slug}/quotas/{self.id}/"

    def set_quota(self, quota: int):
        num_current_tickets = self.tickets.count()
        adjustment = quota - num_current_tickets

        if adjustment < 0:
            self.delete_tickets(-adjustment)
        elif adjustment > 0:
            self.create_tickets(adjustment)

    def delete_tickets(self, num_tickets_to_delete: int):
        from .ticket import Ticket

        logger.info(f"Deleting {num_tickets_to_delete} tickets from {self}")
        tickets_to_delete = self.tickets.filter(order_id__isnull=True).select_for_update()[:num_tickets_to_delete]
        _, deleted_by_model = Ticket.objects.filter(
            event_id=self.event_id,
            id__in=tickets_to_delete.values_list("id", flat=True),
        ).delete()
        num_tickets_deleted = deleted_by_model.get("tickets_v2.Ticket", 0)
        if num_tickets_deleted != num_tickets_to_delete:
            raise ValueError(
                f"Expected to delete {num_tickets_to_delete} tickets, but was only able to delete {num_tickets_deleted}"
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

    def get_counters(self, request: HttpRequest) -> QuotaCounters:
        return QuotaCounters.get_for_event(self.event_id, request)[self.id]

    def can_be_deleted_by(self, request: HttpRequest) -> bool:
        return not self.products.exists() and is_graphql_allowed_for_model(
            request.user,
            instance=self,
            operation="delete",
            field="self",
        )
