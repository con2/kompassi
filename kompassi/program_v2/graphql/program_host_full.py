from collections.abc import Iterable
from dataclasses import dataclass
from itertools import groupby
from typing import Self

import graphene

from kompassi.core.graphql.profile_limited import LimitedProfileType
from kompassi.core.models.person import Person
from kompassi.dimensions.filters import DimensionFilters
from kompassi.involvement.models.involvement import Involvement

from ..models.meta import ProgramV2EventMeta
from ..models.program import Program
from .program_limited import LimitedProgramType


@dataclass
class ProgramHost:
    person: Person
    involvements: list[Involvement]

    @property
    def programs(self) -> list[Program]:
        return [involvement.program for involvement in self.involvements if involvement.program is not None]

    @classmethod
    def from_event(
        cls,
        meta: ProgramV2EventMeta,
        program_filters: DimensionFilters | None = None,
    ) -> Iterable[Self]:
        for person, involvements in groupby(meta.get_active_program_hosts(program_filters), key=lambda x: x.person):
            yield cls(
                person=person,
                involvements=list(involvements),
            )


class FullProgramHostType(graphene.ObjectType):
    """
    Represents a Program Host with access to Person and all their Programs in an Event.
    This is different from Involvement in that an Involvement is related to a single Program
    whereas FullProgramHostType groups all Programs for a Person in an Event.
    """

    person = graphene.NonNull(LimitedProfileType)
    programs = graphene.NonNull(graphene.List(graphene.NonNull(LimitedProgramType)))
