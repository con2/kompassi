from __future__ import annotations

from dataclasses import dataclass
from itertools import groupby

from core.models.event import Event
from dimensions.filters import DimensionFilters

from .invitation import Invitation
from .profile import Profile


@dataclass
class InvolvementEventMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    event: Event

    @property
    def universe(self):
        return self.event.involvement_universe

    @property
    def invitations(self):
        return Invitation.objects.filter(
            survey__event=self.event,
        ).select_related(
            "survey",
            "program",
        )

    def get_people(self, filters: DimensionFilters | None = None) -> list[Profile]:
        if filters is None:
            filters = DimensionFilters()

        involvements = filters.filter(
            self.event.involvements.all()
            .select_related("person", "program", "response")
            .order_by("person__surname", "person__first_name", "-is_active", "id")
        )

        return [
            Profile.from_person_involvements(person, list(person_involvements))
            for person, person_involvements in groupby(involvements, key=lambda inv: inv.person)
        ]
