from collections.abc import Iterable
from dataclasses import dataclass
from itertools import groupby
from typing import Self

import graphene

from core.graphql.person_limited import LimitedPersonType
from core.models.person import Person
from involvement.models.involvement import Involvement

from ..models.meta import ProgramV2EventMeta
from ..models.program import Program
from .program_limited import LimitedProgramType


@dataclass
class ProgramHost:
    person: Person
    involvements: list[Involvement]

    @property
    def programs(self) -> list[Program]:
        return [involvement.program for involvement in self.involvements]

    @classmethod
    def from_event(cls, meta: ProgramV2EventMeta) -> Iterable[Self]:
        for person, involvements in groupby(
            meta.program_hosts.order_by("person"),
            key=lambda x: x.person,
        ):
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

    person = graphene.NonNull(LimitedPersonType)
    programs = graphene.NonNull(graphene.List(graphene.NonNull(LimitedProgramType)))
