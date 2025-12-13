from __future__ import annotations

import logging
import re
from functools import cached_property
from itertools import groupby
from typing import TYPE_CHECKING

from django.db import models

from kompassi.core.models.event import Event
from kompassi.core.utils.log_utils import log_get_or_create
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.dimension_dto import DimensionDTO
from kompassi.dimensions.models.universe import Universe
from kompassi.dimensions.models.universe_annotation import UniverseAnnotation
from kompassi.involvement.dimensions import get_involvement_universe, setup_involvement_dimensions

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
        from kompassi.involvement.emperkelators.desucon2026 import DesuconEmperkelator
        from kompassi.involvement.emperkelators.tracon2025 import TraconEmperkelator

        match = re.match(r"^([a-z-]+)(\d{4})$", self.event.slug)
        if not match:
            return None

        base_slug = match.group(1)
        year = int(match.group(2))

        if base_slug == "tracon" and year >= 2025:
            return TraconEmperkelator
        elif base_slug in ("desucon", "frostbite") and year >= 2026:
            return DesuconEmperkelator
        else:
            return None

    @classmethod
    def ensure(cls, event: Event) -> InvolvementEventMeta:
        universe = get_involvement_universe(event)
        setup_involvement_dimensions(universe, event)

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

        Emperkelator = meta.emperkelator_class
        if Emperkelator is not None:
            DimensionDTO.save_many(
                universe=universe,
                dimension_dtos=Emperkelator.get_dimension_dtos(event),
            )

            annotations = AnnotationDTO.save_many(Emperkelator.get_annotation_dtos())
            UniverseAnnotation.ensure(universe, annotations)

        return meta

    @classmethod
    def get_or_create_dummy(cls) -> tuple[InvolvementEventMeta, bool]:
        event, created = Event.get_or_create_dummy()
        return cls.ensure(event), created

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

    def get_person(self, person_id: int) -> Profile:
        from kompassi.core.models.person import Person

        person = Person.objects.get(id=person_id)
        involvements = (
            self.event.involvements.filter(person=person)
            .select_related("program", "response")
            .order_by("-is_active", "type", "id")
        )

        return Profile.from_person_involvements(person, list(involvements))
