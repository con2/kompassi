from __future__ import annotations

import logging
from functools import cached_property
from itertools import groupby
from typing import TYPE_CHECKING

from django.db import models

from kompassi.core.models.event import Event
from kompassi.core.utils.log_utils import log_get_or_create
from kompassi.dimensions.models.universe import Universe
from kompassi.involvement.dimensions import get_involvement_universe

from ..filters import InvolvementFilters
from .invitation import Invitation
from .profile import Profile
from .registry import Registry

if TYPE_CHECKING:
    from kompassi.involvement.emperkelators.base import BaseEmperkelator

logger = logging.getLogger(__name__)


class InvolvementEventMeta(models.Model):
    event: models.OneToOneField[Event] = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="+",  # reverse being None throws DoesNotExist, we don't want that
    )

    universe: models.OneToOneField[Universe] = models.OneToOneField(
        Universe,
        on_delete=models.CASCADE,
        related_name="+",
    )

    default_registry = models.ForeignKey(
        Registry,
        null=True,  # TODO make non-nullable
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.event.slug if self.event else None

    @property
    def invitations(self):
        return Invitation.objects.filter(
            survey__event=self.event,
        ).select_related(
            "survey",
            "program",
        )

    @cached_property
    def dimension_cache(self):
        return self.event.involvement_universe.preload_dimensions()

    @cached_property
    def emperkelator_class(self) -> type[BaseEmperkelator] | None:
        from kompassi.involvement.emperkelators.tracon2025 import TraconEmperkelator

        match self.event.slug:
            case "tracon2025":
                return TraconEmperkelator
            case _:
                return None

    @classmethod
    def ensure(cls, event: Event) -> InvolvementEventMeta:
        universe = get_involvement_universe(event)

        meta, created = cls.objects.get_or_create(
            event=event,
            defaults=dict(
                universe=universe,
                default_registry=Registry.objects.get_or_create(
                    scope=event.organization.scope,
                    slug="volunteers",
                    defaults=dict(
                        title_en=f"Volunteers of {event.organization.name}",
                        title_fi="{event.organization.name} - Vapaaehtoiset",
                    ),
                )[0],
            ),
        )

        log_get_or_create(logger, meta, created)

        return meta

    def get_people(self, filters: InvolvementFilters | None = None) -> list[Profile]:
        if filters is None:
            filters = InvolvementFilters()

        involvements = filters.filter(
            self.event.involvements.all()
            .select_related("person", "program", "response")
            .order_by("person__surname", "person__first_name", "-is_active", "type", "id")
        )

        return [
            Profile.from_person_involvements(person, list(person_involvements))
            for person, person_involvements in groupby(involvements, key=lambda inv: inv.person)
        ]
