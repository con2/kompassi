from __future__ import annotations

from dataclasses import dataclass

import graphene
from django.db.models import QuerySet, TextField, Value
from django.db.models.functions import Concat, Lower
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_admin
from kompassi.core.merge_people import MergePlan, find_best_candidate, plan_merge
from kompassi.core.utils import normalize_whitespace
from kompassi.event_log_v2.utils.emit import emit

from ..models.person import Person
from .person_admin import AdminPersonType

PEOPLE_LIMIT = 200


@dataclass
class PersonAdminFilters:
    search: str = ""

    def filter(self, queryset: QuerySet[Person]) -> QuerySet[Person]:
        if self.search:
            queryset = queryset.annotate(
                search=Lower(
                    Concat(
                        "first_name",
                        Value(" "),
                        "surname",
                        Value(" "),
                        "nick",
                        Value(" "),
                        "email",
                        Value(" "),
                        "user__username",
                        Value(" #"),
                        "id",
                        output_field=TextField(),
                    )
                ),
            ).filter(search__contains=self.search.lower())

        return queryset


class MergeReferenceType(graphene.ObjectType):
    model = graphene.NonNull(graphene.String)
    field = graphene.NonNull(graphene.String)
    count = graphene.NonNull(graphene.Int)


class MergeConflictType(graphene.ObjectType):
    model = graphene.NonNull(graphene.String)
    field = graphene.NonNull(graphene.String)
    person_id = graphene.NonNull(graphene.Int)
    description = graphene.NonNull(graphene.String)


class PersonMergePreviewType(graphene.ObjectType):
    into = graphene.NonNull(AdminPersonType)
    people = graphene.NonNull(graphene.List(graphene.NonNull(AdminPersonType)))
    references = graphene.NonNull(graphene.List(graphene.NonNull(MergeReferenceType)))
    conflicts = graphene.NonNull(graphene.List(graphene.NonNull(MergeConflictType)))
    can_merge = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_people(plan: MergePlan, info):
        return [plan.into, *plan.mergees]


def resolve_merge_plan(person_ids: list[int], into_person_id: int | None) -> MergePlan:
    """
    Builds the plan for merging `person_ids` into `into_person_id`, or into the best
    candidate among them when no survivor is given. Shared by the preview query and the
    mutation so both always agree on what a merge would do.
    """
    people = list(Person.objects.filter(id__in=person_ids).select_related("user"))
    if len(people) != len(set(person_ids)) or len(people) < 2:
        raise Person.DoesNotExist("at least two distinct existing people are required")

    if into_person_id is None:
        into, mergees = find_best_candidate(people)
    else:
        into = next((person for person in people if person.pk == into_person_id), None)
        if into is None:
            raise Person.DoesNotExist("the surviving person must be one of the people to merge")
        mergees = [person for person in people if person.pk != into_person_id]

    return plan_merge(into, mergees)


class AdminType(graphene.ObjectType):
    """
    Site-wide administration. Every field checks the admin CBAC claims, which only
    a superuser sudo grants (see graphql_check_admin).
    """

    @staticmethod
    def resolve_people(root, info, search: str = "", return_none: bool = False):
        """
        People matching the search, or nothing when `returnNone` is set. The list is
        capped at PEOPLE_LIMIT rows, so narrow the search when the cap is hit.
        """
        graphql_check_admin(info, model="Person")

        if return_none:
            return []

        queryset = Person.objects.all().select_related("user").order_by("surname", "first_name", "id")
        return PersonAdminFilters(search=search).filter(queryset)[:PEOPLE_LIMIT]

    people = graphene.NonNull(
        graphene.List(graphene.NonNull(AdminPersonType)),
        search=graphene.String(default_value=""),
        return_none=graphene.Boolean(default_value=False),
        description=normalize_whitespace(resolve_people.__doc__ or ""),
    )

    @staticmethod
    def resolve_person(root, info, id: int):
        graphql_check_admin(info, model="Person")

        request: HttpRequest = info.context
        person = Person.objects.select_related("user").get(id=id)
        emit("core.person.viewed", request=request, person=person.pk)
        return person

    person = graphene.Field(AdminPersonType, id=graphene.Int(required=True))

    @staticmethod
    def resolve_merge_preview(root, info, person_ids: list[int], into_person_id: int | None = None):
        """
        What merging the given people would move and which records would collide.
        The survivor defaults to the best candidate among them.
        """
        graphql_check_admin(info, model="Person", operation="update")
        return resolve_merge_plan(person_ids, into_person_id)

    merge_preview = graphene.NonNull(
        PersonMergePreviewType,
        person_ids=graphene.NonNull(graphene.List(graphene.NonNull(graphene.Int))),
        into_person_id=graphene.Int(),
        description=normalize_whitespace(resolve_merge_preview.__doc__ or ""),
    )
