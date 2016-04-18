from django.conf import settings
from django.contrib.contenttypes.models import ContentType


IDENTICAL_FIELDS_REQUIRED_FOR_MERGE = (
    'first_name',
    'surname',
    'nick',
    'email',
)


def make_key(person):
    return tuple(getattr(person, field.lower()) for field in IDENTICAL_FIELDS_REQUIRED_FOR_MERGE)


def possible_merges(people):
    key_map = dict()

    for person in people:
        key = make_key(person)
        key_map.setdefault(key, [])
        key_map[key].append(person)

    result = []

    for unused, people_to_merge in key_map.iteritems():
        if len(people_to_merge) > 1:
            person_to_spare, people_to_merge = find_best_candidate(people_to_merge)
            result.append((person_to_spare, people_to_merge))

    return result


def find_best_candidate(people_to_merge):
    people_to_merge = list(people_to_merge)
    people_to_merge.sort(cmp=compare_persons)
    person_to_spare = people_to_merge.pop()
    return person_to_spare, people_to_merge


def compare_persons(left, right):
    # If only one has .user, it's better
    if left.user is not None and right.user is None:
        return 1
    if right.user is not None and left.user is None:
        return -1

    # If both have users, return the one whose user was created first
    if left.user is not None and right.user is not None:
        return cmp(left.user.pk, right.user.pk)

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
    return cmp(left.pk, right.pk)


def rewrite_references(old, new):
    assert old.__class__ is new.__class__
    HostModel = old.__class__

    for content_type in ContentType.objects.all():
        ReferringModel = content_type.model_class()
        for field in ReferringModel._meta.fields:
            if field.related_model is Person:
                filter_kwargs = {f.name: old}
                update_kwargs = {f.name: new}
                ReferringModel.objects.filter(**filter_kwargs).update(**update_kwargs)


def merge_people(people_to_merge, into):
    for mergee in people_to_merge:
        if into.user is None and mergee.user is not None:
            into.user = mergee.user
            mergee.user = None
        else:
            rewrite_references(mergee.user, into.user)

        rewrite_references(mergee, into)

        # All references are updated, so this should be safe
        mergee.delete()
