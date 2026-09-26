"""
Combining duplicate accounts (Person and its User) of the same real person into one.

`plan_merge` computes what a merge would move and what would collide; `merge_people` refuses
to run when the plan has conflicts. The conflict rule is deliberately strict: a duplicate is
only combined when nothing on it could clash with the survivor, and the operator resolves any
clash by hand first.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import cmp_to_key, lru_cache
from typing import Any

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Model, Q, UniqueConstraint
from django.db.transaction import atomic
from django.http import HttpRequest

from kompassi.core.models import Person
from kompassi.event_log_v2.utils.emit import emit

logger = logging.getLogger(__name__)


IDENTICAL_FIELDS_REQUIRED_FOR_MERGE = (
    "first_name",
    "surname",
    "nick",
    "email",
)


# Records the code treats as one-per-person without a database constraint enforcing it.
# Each row is (model label, person field, columns that identify the record, extra filter).
# Kept in one place so a new implicit singleton can be added by whoever notices it.
SINGLETON_KEYS: tuple[tuple[str, str, tuple[str, ...], dict[str, Any]], ...] = (
    ("labour.Signup", "person", ("event",), {}),
    ("badges.Badge", "person", ("personnel_class__event",), {"revoked_at__isnull": True}),
    ("involvement.Involvement", "person", ("universe", "app", "type", "program", "response"), {}),
)

# Records that only say "this person has X" and carry no data of their own. When both
# accounts have the same one, the duplicate's row is dropped instead of reported as a
# conflict, like a many-to-many membership. Each row is (model label, person field,
# columns that identify the record).
MEMBERSHIP_KEYS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("labour.PersonQualification", "person", ("qualification",)),
    ("labour.SurveyRecord", "person", ("survey",)),
)


def make_key(person):
    return tuple(getattr(person, field.lower()) for field in IDENTICAL_FIELDS_REQUIRED_FOR_MERGE)


@dataclass(frozen=True)
class ReferenceField:
    model: type[Model]
    field_name: str

    @property
    def label(self) -> str:
        meta = self.model._meta
        return f"{meta.app_label}.{meta.object_name}"

    @property
    def is_membership(self) -> bool:
        """
        An auto-created many-to-many through table (groups, favorites, subscriptions)
        holds set membership, so the same row on both accounts is a duplicate to drop,
        never a conflict.
        """
        return bool(self.model._meta.auto_created)

    def unique_column_sets(self) -> list[tuple[str, ...]]:
        """
        Column sets that must be unique together and include this field.
        A conditional UniqueConstraint is treated as unconditional, which can only
        report a conflict that would not have failed, never miss one that would.
        """
        meta = self.model._meta
        result: list[tuple[str, ...]] = []

        if getattr(meta.get_field(self.field_name), "unique", False):
            result.append((self.field_name,))

        for columns in meta.unique_together:
            if self.field_name in columns:
                result.append(tuple(columns))

        for constraint in meta.constraints:
            if isinstance(constraint, UniqueConstraint) and self.field_name in constraint.fields:
                result.append(tuple(constraint.fields))

        return result


@lru_cache
def get_reference_fields(related_model: type[Model] = Person) -> tuple[ReferenceField, ...]:
    """
    Returns the foreign keys and one-to-one fields of all models, including
    auto-created many-to-many through tables, that reference the given model.
    """
    reference_fields = []

    for model in apps.get_models(include_auto_created=True):
        meta = model._meta

        if meta.proxy:
            continue

        for model_field in meta.get_fields():
            if (
                model_field.concrete
                and not model_field.many_to_many
                and not model_field.auto_created
                and model_field.related_model is related_model
            ):
                reference_fields.append(ReferenceField(model, model_field.name))

    return tuple(reference_fields)


def possible_merges(people):
    key_map = dict()

    for person in people:
        key = make_key(person)
        key_map.setdefault(key, [])
        key_map[key].append(person)

    result = []

    for people_to_merge in key_map.values():
        if len(people_to_merge) > 1:
            person_to_spare, people_to_merge = find_best_candidate(people_to_merge)
            result.append((person_to_spare, people_to_merge))

    return result


def find_best_candidate(people_to_merge: Iterable[Person]) -> tuple[Person, list[Person]]:
    people_to_merge = sorted(people_to_merge, key=cmp_to_key(compare_persons))
    person_to_spare = people_to_merge.pop()
    return person_to_spare, people_to_merge


def compare_persons(left, right) -> int:
    # If only one has .user, it's better
    if left.user is not None and right.user is None:
        return 1
    if right.user is not None and left.user is None:
        return -1

    # If only one has phone number, it's better
    if left.phone and not right.phone:
        return 1
    if right.phone and not left.phone:
        return -1

    # If only one has email address, it's better
    if left.email and not right.email:
        return 1
    if right.email and not left.email:
        return -1

    # Otherwise the newer the better
    if left.pk > right.pk:
        return -1
    if right.pk > left.pk:
        return 1
    return 0


@dataclass(frozen=True)
class MergeReference:
    model: str
    field: str
    count: int


@dataclass(frozen=True)
class MergeConflict:
    model: str
    field: str
    person_id: int
    description: str


@dataclass
class MergePlan:
    into: Person
    mergees: list[Person]
    references: list[MergeReference] = field(default_factory=list)
    conflicts: list[MergeConflict] = field(default_factory=list)

    @property
    def can_merge(self) -> bool:
        return not self.conflicts


class MergeConflictError(Exception):
    def __init__(self, plan: MergePlan):
        super().__init__(f"{len(plan.conflicts)} records would collide with the surviving account")
        self.plan = plan


def _referencing_rows(reference: ReferenceField, instance: Model, extra: dict[str, Any] | None = None):
    return reference.model._default_manager.filter(**{reference.field_name: instance}, **(extra or {}))


def _count_references(target_model: type[Model], mergee: Model, skip: ReferenceField | None) -> list[MergeReference]:
    result = []
    for reference in get_reference_fields(target_model):
        if reference == skip:
            continue
        count = _referencing_rows(reference, mergee).count()
        if count:
            result.append(MergeReference(model=reference.label, field=reference.field_name, count=count))
    return result


def _find_conflicts(
    reference: ReferenceField,
    mergee: Model,
    into: Model,
    person_id: int,
    columns: tuple[str, ...],
    extra: dict[str, Any] | None = None,
) -> list[MergeConflict]:
    """
    Reports each of the mergee's rows for which the survivor already has a row with
    the same values in `columns`. Either instance may be a Person or a User.
    """
    other_columns = tuple(column for column in columns if column != reference.field_name)
    mergee_rows = _referencing_rows(reference, mergee, extra)
    into_rows = _referencing_rows(reference, into, extra)

    def conflict(description: str) -> MergeConflict:
        return MergeConflict(
            model=reference.label,
            field=reference.field_name,
            person_id=person_id,
            description=description,
        )

    if not other_columns:
        # The field alone is unique, so both having any row at all is a collision.
        return [conflict("one per person")] if mergee_rows.exists() and into_rows.exists() else []

    return [
        conflict(", ".join(f"{column}={value}" for column, value in row.items()))
        for row in mergee_rows.values(*other_columns)
        if into_rows.filter(**row).exists()
    ]


def _plan_instance(
    plan: MergePlan,
    target_model: type[Model],
    mergee: Model,
    into: Model | None,
    person_id: int,
    skip: ReferenceField | None = None,
):
    plan.references.extend(_count_references(target_model, mergee, skip))

    if into is None:
        # The survivor has no User: the mergee's User is adopted rather than re-pointed,
        # so nothing of it can collide.
        return

    for reference in get_reference_fields(target_model):
        if reference == skip or reference.is_membership:
            continue
        for columns in reference.unique_column_sets():
            plan.conflicts.extend(_find_conflicts(reference, mergee, into, person_id, columns))

    if target_model is Person:
        for model_label, field_name, columns, extra in SINGLETON_KEYS:
            reference = ReferenceField(apps.get_model(model_label), field_name)
            plan.conflicts.extend(_find_conflicts(reference, mergee, into, person_id, (field_name, *columns), extra))


def plan_merge(into: Person, mergees: list[Person]) -> MergePlan:
    """
    Computes, without writing anything, what merging `mergees` into `into` would
    re-point and which records would collide with the survivor's.
    """
    if into in mergees:
        raise ValueError("the surviving person cannot also be merged")
    if len({person.pk for person in mergees}) != len(mergees):
        raise ValueError("the same person cannot be merged twice")

    User = get_user_model()
    person_user_field = ReferenceField(Person, "user")
    plan = MergePlan(into=into, mergees=list(mergees))
    surviving_user = into.user

    for mergee in mergees:
        _plan_instance(plan, Person, mergee, into, mergee.pk)

        if mergee.user is not None:
            _plan_instance(plan, User, mergee.user, surviving_user, mergee.pk, skip=person_user_field)
            if surviving_user is None:
                surviving_user = mergee.user

    return plan


def _repoint(target_model: type[Model], mergee: Model, into: Model, skip: ReferenceField | None = None):
    for reference in get_reference_fields(target_model):
        if reference == skip:
            continue
        logger.debug(
            "Re-pointing references",
            extra=dict(model=reference.label, field=reference.field_name, mergee=mergee.pk, into=into.pk),
        )
        if reference.is_membership:
            for columns in reference.unique_column_sets():
                _drop_duplicate_memberships(reference, mergee, into, columns)
        if target_model is Person:
            for model_label, field_name, columns in MEMBERSHIP_KEYS:
                if reference == ReferenceField(apps.get_model(model_label), field_name):
                    _drop_duplicate_memberships(reference, mergee, into, (field_name, *columns))
        _referencing_rows(reference, mergee).update(**{reference.field_name: into})


def _drop_duplicate_memberships(reference: ReferenceField, mergee: Model, into: Model, columns: tuple[str, ...]):
    other_columns = tuple(column for column in columns if column != reference.field_name)
    for row in _referencing_rows(reference, into).values(*other_columns):
        _referencing_rows(reference, mergee).filter(**row).delete()


def _repoint_event_log_entries(mergee: Person, into: Person):
    from kompassi.event_log_v2.models import Entry

    # The person id may have been stored as an int or a str depending on the emitter.
    entries = Entry.objects.filter(Q(other_fields__person=mergee.pk) | Q(other_fields__person=str(mergee.pk)))
    for entry in entries:
        entry.other_fields["person"] = into.pk
        entry.save(update_fields=["other_fields"])


@atomic
def merge_people(into: Person, mergees: list[Person], *, request: HttpRequest | None = None) -> MergePlan:
    """
    Moves everything that refers to any of `mergees` or their Users onto `into` and deletes
    the duplicates. Raises MergeConflictError, changing nothing, if the plan has conflicts.
    """
    plan = plan_merge(into, mergees)
    if not plan.can_merge:
        raise MergeConflictError(plan)

    User = get_user_model()
    person_user_field = ReferenceField(Person, "user")
    merged_ids = [mergee.pk for mergee in mergees]

    for mergee in mergees:
        mergee_user = mergee.user

        if mergee_user is not None:
            # Detached with a bare update: Person.save() would push the mergee's name and
            # email into the User it is about to lose.
            Person.objects.filter(pk=mergee.pk).update(user=None)

        _repoint(Person, mergee, into)
        _repoint_event_log_entries(mergee, into)
        mergee.delete()

        if mergee_user is None:
            continue

        if into.user is None:
            into.user = mergee_user
            into.save()
        else:
            _repoint(User, mergee_user, into.user, skip=person_user_field)
            mergee_user.delete()

    into.refresh_from_db()
    into.save()
    if into.user is not None:
        into.apply_state()
    else:
        into.apply_state_update_badges()

    emit(
        "core.person.merged",
        request=request,
        person=into.pk,
        merged=merged_ids,
        references=[
            dict(model=reference.model, field=reference.field, count=reference.count) for reference in plan.references
        ],
    )

    return plan
