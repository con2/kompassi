from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import graphene
from django.contrib.auth import get_user_model
from django.core.paginator import Page
from django.db import models

from kompassi.core.models.event import Event
from kompassi.core.models.organization import Organization
from kompassi.core.models.person import Person
from kompassi.graphql_api.pagination import PaginationInput, PaginationType

from .. import registry
from ..filters import EventLogFilters
from ..models.entry import Entry
from .entry_limited import LimitedEventLogEntryType

User = get_user_model()


@dataclass
class EventLog:
    event: Event
    organization: Organization
    filters: EventLogFilters
    pagination: PaginationInput

    @cached_property
    def scoped_entries(self) -> models.QuerySet[Entry]:
        return Entry.for_event_and_organization(self.event, self.organization)

    @cached_property
    def page(self) -> Page:
        queryset = self.filters.filter(self.scoped_entries).select_related("actor__person").order_by("-id")
        return self.pagination.paginate(queryset)


class EventLogDimensionValueType(graphene.ObjectType):
    slug = graphene.NonNull(graphene.String)
    title = graphene.NonNull(graphene.String)


class EventLogDimensionType(graphene.ObjectType):
    slug = graphene.NonNull(graphene.String)
    values = graphene.NonNull(graphene.List(graphene.NonNull(EventLogDimensionValueType)))


class EventLogType(graphene.ObjectType):
    @staticmethod
    def resolve_entries(event_log: EventLog, info):
        entries = list(event_log.page.object_list)
        Entry.prefetch_referenced_objects(entries)
        return entries

    entries = graphene.NonNull(graphene.List(graphene.NonNull(LimitedEventLogEntryType)))

    @staticmethod
    def resolve_pagination(event_log: EventLog, info):
        return PaginationType.from_page(event_log.page)

    pagination = graphene.NonNull(PaginationType)

    @staticmethod
    def resolve_dimensions(event_log: EventLog, info):
        month_values = [
            EventLogDimensionValueType(slug=f"{year}-{month:02}", title=f"{year}-{month:02}")
            for (year, month) in Entry.get_expected_partitions(months_future=0)
        ]

        entry_type_values = [
            EventLogDimensionValueType(slug=slug, title=slug) for slug in sorted(registry.entry_types.keys())
        ]

        # The actor dropdown always reflects the selected month, regardless of the
        # entry_type/actor filters, so it never empties itself out from under the user.
        month_queryset = event_log.filters.filter_month(event_log.scoped_entries)
        # order_by() clears Entry's default id ordering: left in place, Django adds id to
        # the SELECT to keep it satisfying ORDER BY, so DISTINCT stops deduplicating by
        # actor_id alone.
        actor_ids = list(month_queryset.exclude(actor_id=None).order_by().values_list("actor_id", flat=True).distinct())

        full_names_by_user_id = {
            person.user_id: person.full_name for person in Person.objects.filter(user_id__in=actor_ids)
        }
        usernames_by_user_id = dict(User.objects.filter(id__in=actor_ids).values_list("id", "username"))
        actor_values = [
            EventLogDimensionValueType(
                slug=str(user_id),
                title=full_names_by_user_id.get(user_id, usernames_by_user_id.get(user_id, str(user_id))),
            )
            for user_id in actor_ids
        ]

        return [
            EventLogDimensionType(slug="month", values=month_values),
            EventLogDimensionType(slug="type", values=entry_type_values),
            EventLogDimensionType(slug="actor", values=actor_values),
        ]

    dimensions = graphene.NonNull(graphene.List(graphene.NonNull(EventLogDimensionType)))
