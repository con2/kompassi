from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Self

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.db import models
from django.http import QueryDict
from django.utils.timezone import now

from dimensions.filters import DimensionFilters
from dimensions.graphql.dimension_filter_input import DimensionFilterInput
from forms.models.response import Response
from forms.utils.process_form_data import FALSY_VALUES

from .models.program import Program
from .models.schedule_item import ScheduleItem


def ensure_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt


def parse_datetime(s: str) -> datetime:
    """
    If there is no timezone info, assume UTC.
    """
    return ensure_aware(datetime.fromisoformat(s))


class ProgramUserRelation(Enum):
    FAVORITED = "FAVORITED"
    # SIGNED_UP = "SIGNED_UP"
    HOSTING = "HOSTING"


@dataclass
class ProgramFilters:
    slugs: list[str] | None = None
    hide_past: bool = False
    updated_after: datetime | None = None
    dimension_filters: DimensionFilters = field(default_factory=DimensionFilters)
    user_relation: ProgramUserRelation | None = None

    @classmethod
    def from_query_dict(
        cls,
        filters: QueryDict | dict[str, list[str]],
    ) -> Self:
        if isinstance(filters, QueryDict):
            filters = {k: [str(v) for v in vs] for k, vs in filters.lists()}

        filters = {
            dimension_slug: [slug for slugs in value_slugs for slug in slugs.split(",")]
            for (dimension_slug, value_slugs) in filters.items()
        }

        # filter programs by slug (may be ?slug=a&slug=b or ?slug=a,b,c)
        slugs = filters.pop("slug", [])
        hide_past = all(v.lower() in FALSY_VALUES for v in filters.pop("past", []))

        user_relations = [ProgramUserRelation(rel.upper()) for rel in filters.pop("relation", [])]
        if len(user_relations) > 1:
            raise ValueError("Only one user relation can be specified.")
        user_relation = user_relations[0] if user_relations else None

        updated_after = (
            parse_datetime(updated_after_str)
            if (updated_after_strs := filters.pop("updated_after", []))
            and (updated_after_str := max(updated_after_strs))
            else None
        )

        return cls(
            slugs=slugs,
            dimension_filters=DimensionFilters(filters=filters),
            user_relation=user_relation,
            hide_past=hide_past,
            updated_after=updated_after,
        )

    @classmethod
    def from_graphql(
        cls,
        filters: list[DimensionFilterInput] | None,
        hide_past: bool = False,
        user_relation: ProgramUserRelation | None = None,
        updated_after: datetime | None = None,
    ):
        return cls(
            dimension_filters=DimensionFilters.from_graphql(filters),
            user_relation=user_relation,
            hide_past=hide_past,
            updated_after=ensure_aware(updated_after) if updated_after else None,
        )

    def filter_program(
        self,
        programs: models.QuerySet[Program],
        user: AbstractBaseUser | AnonymousUser | None = None,
        t: datetime | None = None,
    ):
        if self.slugs:
            programs = programs.filter(slug__in=self.slugs)

        if self.user_relation:
            if user and user.is_authenticated and (person := user.person):  # type: ignore
                match self.user_relation:
                    case ProgramUserRelation.FAVORITED:
                        programs = programs.filter(schedule_items__favorited_by=user)
                    case ProgramUserRelation.HOSTING:
                        programs = programs.filter(
                            involvements__person=person,
                            involvements__is_active=True,
                        )
                    case _:
                        raise NotImplementedError(self.user_relation)
            else:
                return programs.none()

        programs = self.dimension_filters.filter(
            programs,
            field_name="cached_combined_dimensions",
        )

        if self.hide_past:
            if t is None:
                t = now()
            programs = programs.filter(cached_latest_end_time__gte=t)

        if self.updated_after:
            programs = programs.filter(updated_at__gt=self.updated_after)

        return (
            programs.distinct()
            .select_related("event")
            .prefetch_related(
                "schedule_items",
                "schedule_items__cached_event",
            )
            .order_by("cached_earliest_start_time")
        )

    def filter_schedule_items(
        self,
        schedule_items: models.QuerySet[ScheduleItem],
        user: AbstractBaseUser | AnonymousUser | None = None,
        t: datetime | None = None,
    ):
        if self.slugs:
            schedule_items = schedule_items.filter(slug__in=self.slugs)

        if self.user_relation:
            if user and user.is_authenticated and (person := user.person):  # type: ignore
                match self.user_relation:
                    case ProgramUserRelation.FAVORITED:
                        schedule_items = schedule_items.filter(favorited_by=user)
                    case ProgramUserRelation.HOSTING:
                        schedule_items = schedule_items.filter(
                            program__involvements__person=person,
                            program__involvements__is_active=True,
                        )
                    case _:
                        raise NotImplementedError(self.user_relation)
            else:
                return schedule_items.none()

        schedule_items = self.dimension_filters.filter(
            schedule_items,
            field_name="cached_combined_dimensions",
        )

        if self.hide_past:
            if t is None:
                t = now()
            schedule_items = schedule_items.filter(cached_end_time__gte=t)

        if self.updated_after:
            schedule_items = schedule_items.filter(updated_at__gt=self.updated_after)

        return (
            schedule_items.distinct()
            .select_related(
                "cached_event",
                "program__event",
                "program",
            )
            .order_by("start_time")
        )

    def filter_program_offers(
        self,
        program_offers: models.QuerySet[Response],
        user: AbstractBaseUser | AnonymousUser | None = None,
    ):
        if self.slugs:
            return program_offers.none()

        if self.user_relation:
            if user and user.is_authenticated:
                match self.user_relation:
                    case ProgramUserRelation.FAVORITED:
                        program_offers = program_offers.none()
                    case ProgramUserRelation.HOSTING:
                        program_offers = program_offers.filter(revision_created_by=user)
                    case _:
                        raise NotImplementedError(self.user_relation)
            else:
                return program_offers.none()

        return self.dimension_filters.filter(program_offers)
