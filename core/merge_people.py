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

    # Otherwise the newer the better
    return cmp(left.pk, right.pk)


def merge_people(people_to_merge, into):
    for mergee in people_to_merge:
        assert mergee.user is None

        for app_label, model_name in [
            ('badges', 'badge'),
            ('labour', 'personqualification'),
            ('labour', 'signup'),
            ('mailings', 'personmessage'),
            ('programme', 'programmerole'),
        ]:
            if app_label in settings.INSTALLED_APPS:
                Model = ContentType.objects.get_by_natural_key(app_label, model_name).model_class()
                Model.objects.filter(person=mergee).update(person=into)

        # All references are updated, so this should be safe
        mergee.delete()
