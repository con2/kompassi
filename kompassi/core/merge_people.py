import logging
from functools import lru_cache

from django.contrib.contenttypes.models import ContentType
from django.db.transaction import atomic

from kompassi.core.models import Person

logger = logging.getLogger(__name__)


IDENTICAL_FIELDS_REQUIRED_FOR_MERGE = (
    "first_name",
    "surname",
    "nick",
    "email",
)


def make_key(person):
    return tuple(getattr(person, field.lower()) for field in IDENTICAL_FIELDS_REQUIRED_FOR_MERGE)


@lru_cache
def get_reference_fields(related_model=Person):
    """
    Returns ForeignKeys, OneToOneFields and ManyToManyFields that reference the given model.
    """
    reference_fields = []

    for content_type in ContentType.objects.all():
        ModelClass = content_type.model_class()

        if not ModelClass:
            # wtf is south.migrationhistory still doing in our database?
            logger.warning(
                "get_reference_fields: ContentType without ModelClass: %s.%s", content_type.app_label, content_type.name
            )
            continue

        meta = ModelClass._meta

        if meta.proxy or meta.abstract:
            continue

        for field in meta.get_fields():
            if field.concrete and not field.auto_created and field.related_model is related_model:
                reference_fields.append((ModelClass, field))

    return reference_fields


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


def find_best_candidate(people_to_merge):
    people_to_merge = list(people_to_merge)
    people_to_merge.sort(cmp=compare_persons)
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


@atomic
def merge_people(people_to_merge, into):
    for mergee in people_to_merge:
        if mergee.user and into.user:
            merge(mergee.user, into.user)

        merge(mergee, into)


def merge(mergee, into):
    """
    Updates all references to `mergee` to point to `into` and deletes `mergee`.
    """
    ModelClass = mergee._meta.model
    if into._meta.model is not ModelClass:
        raise AssertionError("thou shalt not merge instances of different models")

    for RelatedModel, field in get_reference_fields(ModelClass):
        if field.many_to_many:
            RelatedModel = getattr(RelatedModel, field.name).through

        criteria = {field.name: mergee}
        update = {field.name: into}

        logger.debug("Updating %s by %r with %r", RelatedModel, criteria, update)

        RelatedModel.objects.filter(**criteria).update(**update)

    mergee.delete()
