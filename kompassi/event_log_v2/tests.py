from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import pytest
from django.contrib.auth import get_user_model

from kompassi.core.models.event import Event
from kompassi.core.models.organization import Organization
from kompassi.core.models.venue import Venue
from kompassi.tickets_v2.optimized_server.utils.uuid7 import uuid7

from .filters import EventLogFilters
from .models.entry import Entry

User = get_user_model()


@pytest.mark.django_db
def test_for_event_and_organization_scope():
    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    other_organization = Organization.objects.create(slug="other-organization", name="Other organization")
    other_venue, _created = Venue.get_or_create_dummy()
    other_event, _created = Event.objects.get_or_create(
        slug="other-event",
        defaults=dict(name="Other event", organization=other_organization, venue=other_venue),
    )

    event_entry = Entry.objects.create(entry_type="core.event.created", other_fields={"event": event.slug})
    organization_entry = Entry.objects.create(
        entry_type="core.event.created",
        other_fields={"organization": event.organization.slug},
    )
    cbac_event_entry = Entry.objects.create(
        entry_type="access.cbac.denied",
        other_fields={"claims": {"event": event.slug, "app": "involvement"}},
    )
    cbac_organization_entry = Entry.objects.create(
        entry_type="access.cbac.denied",
        other_fields={"claims": {"organization": event.organization.slug, "app": "involvement"}},
    )

    other_organization_entry = Entry.objects.create(
        entry_type="core.event.created",
        other_fields={"event": other_event.slug, "organization": other_organization.slug},
    )
    claims_only_non_cbac_entry = Entry.objects.create(
        entry_type="core.event.created",
        other_fields={"claims": {"event": event.slug}},
    )

    entries = set(Entry.for_event_and_organization(event, event.organization).values_list("id", flat=True))

    assert entries == {event_entry.id, organization_entry.id, cbac_event_entry.id, cbac_organization_entry.id}
    assert other_organization_entry.id not in entries
    assert claims_only_non_cbac_entry.id not in entries


@pytest.mark.django_db
def test_for_event_and_organization_orders_newest_first():
    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    now = datetime.now(UTC)

    first = Entry.objects.create(
        id=uuid7(now),
        entry_type="core.event.created",
        other_fields={"event": event.slug},
    )
    second = Entry.objects.create(
        id=uuid7(now + timedelta(seconds=1)),
        entry_type="core.event.created",
        other_fields={"event": event.slug},
    )

    entries = list(
        EventLogFilters().filter(Entry.for_event_and_organization(event, event.organization)).order_by("-id")
    )

    assert [entry.id for entry in entries] == [second.id, first.id]


@pytest.mark.django_db
def test_actor_filter_system_sentinel_selects_entries_without_an_actor():
    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    actor = User.objects.create(username="event-log-test-actor")

    with_actor = Entry.objects.create(
        entry_type="core.event.created",
        actor=actor,
        other_fields={"event": event.slug},
    )
    without_actor = Entry.objects.create(
        entry_type="core.event.created",
        other_fields={"event": event.slug},
    )
    scoped = Entry.for_event_and_organization(event, event.organization)

    system_only = EventLogFilters(actor=["system"]).filter(scoped)
    assert set(system_only.values_list("id", flat=True)) == {without_actor.id}

    actor_only = EventLogFilters(actor=[str(actor.id)]).filter(scoped)
    assert set(actor_only.values_list("id", flat=True)) == {with_actor.id}

    both = EventLogFilters(actor=[str(actor.id), "system"]).filter(scoped)
    assert set(both.values_list("id", flat=True)) == {with_actor.id, without_actor.id}


def test_event_log_filters_from_graphql_defaults_month_to_current():
    filters = EventLogFilters.from_graphql(None)

    assert filters.month is None
    assert filters.entry_type == []
    assert filters.actor == []


@dataclass
class _FakeDimensionFilterInput:
    """Stands in for the graphene-constructed DimensionFilterInput in GraphQL requests."""

    dimension: str
    values: list[str] | None


def test_event_log_filters_from_graphql_parses_known_slugs():
    filters = EventLogFilters.from_graphql(
        [
            _FakeDimensionFilterInput("month", ["2026-01"]),
            _FakeDimensionFilterInput("type", ["core.event.created"]),
            _FakeDimensionFilterInput("actor", ["42"]),
            _FakeDimensionFilterInput("unknown", ["ignored"]),
        ]
    )

    assert filters.month == "2026-01"
    assert filters.entry_type == ["core.event.created"]
    assert filters.actor == ["42"]
    assert filters.year_month == (2026, 1)
