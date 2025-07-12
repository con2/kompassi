import logging
from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from functools import cached_property
from typing import Any, Self
from uuid import UUID

from django.conf import settings
from django.db import models
from pydantic import BaseModel

from core.models import Event, Organization, Person
from tickets_v2.optimized_server.utils.uuid7 import uuid7, uuid7_month_range_for_year_month, uuid7_to_datetime

from ..utils.monthly_partitions import MonthlyPartitionsMixin

logger = logging.getLogger("kompassi")


class Entry(MonthlyPartitionsMixin, models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=False,
        related_name="access_log_entries",
    )
    entry_type = models.CharField(max_length=255)
    other_fields = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ("id",)

    @cached_property
    def meta(self):
        from .. import registry

        return registry.get(self.entry_type)

    @cached_property
    def message_vars(self):
        return dict(
            self.other_fields,
            event=self.event,
            organization=self.organization,
            actor=self.actor.username if self.actor is not None else None,
            actor_display_name=self.actor.get_full_name() if self.actor is not None else None,
            actor_email=self.actor.email if self.actor is not None else None,
            created_at=self.created_at,
            entry_type=self.entry_type,
            person=self.person,
            default_from_email=settings.DEFAULT_FROM_EMAIL,
        )

    @cached_property
    def message(self):
        try:
            if callable(self.meta.message):
                return self.meta.message(self)
            else:
                return self.meta.message.format(**self.message_vars)
        except Exception as e:
            logger.exception(f"Error formatting message for event log entry {self.pk}")
            return f"An error occurred while formatting the message: {e}"

    def __str__(self):
        return self.message

    @cached_property
    def created_at(self):
        return uuid7_to_datetime(self.id)

    @property
    def created_by(self):
        return self.actor

    @cached_property
    def event(self):
        if event_slug := self.other_fields.get("event"):
            return Event.objects.get(slug=event_slug)
        return None

    @cached_property
    def organization(self):
        if org_slug := self.other_fields.get("organization"):
            return Organization.objects.get(slug=org_slug)
        if event := self.event:
            return event.organization
        return None

    @cached_property
    def person(self):
        if person_id := self.other_fields.get("person"):
            return Person.objects.get(id=person_id)
        return None

    @classmethod
    def year_month_filter(cls, queryset: models.QuerySet[Self], year: int, month: int) -> models.QuerySet[Self]:
        start, end = uuid7_month_range_for_year_month(year, month)
        return queryset.filter(id__gte=start, id__lt=end)

    @classmethod
    def conform(cls, value: Any) -> Any:
        """
        Conform the value to a type that can be stored in the database.
        """
        if slug := getattr(value, "slug", None):
            value = slug
        elif id := getattr(value, "id", None):
            value = id
        elif isinstance(value, Enum):
            value = value.value

        # encode safe complex types as strings
        if isinstance(value, UUID):
            value = str(value)
        elif isinstance(value, (datetime, date)):
            value = value.isoformat()
        elif isinstance(value, BaseModel):
            value = value.model_dump(
                mode="json",
                by_alias=True,
                exclude_none=True,
            )

        return value

    @classmethod
    def hoist(cls, attrs: Mapping[str, Any]):
        """
        Given a dictionary of potential kwargs to the constructor, separate relational fields
        and the rest that will be shoved into other_fields.
        """
        other_fields = dict(attrs)
        attrs = dict()

        if "other_fields" in other_fields:
            other_fields.update(other_fields.pop("other_fields"))
        if "created_at" in other_fields:
            attrs["created_at"] = other_fields.pop("created_at")
        if "actor" in other_fields:
            attrs["actor"] = other_fields.pop("actor")
        if "entry_type" in other_fields:
            attrs["entry_type"] = other_fields.pop("entry_type")

        other_fields = {k: cv for (k, v) in other_fields.items() if (cv := cls.conform(v)) not in (None, "")}

        return attrs, other_fields
