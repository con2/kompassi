

IDENTICAL_FIELDS_REQUIRED_FOR_MERGE = (
    'first_name',
    'surname',
    'nick',
    'email',
)


def make_key(person):
    return [getattr(person, field) for field in IDENTICAL_FIELDS_REQUIRED_FOR_MERGE]


def possible_merges(people):
    key_map = dict()

    for person in people:
        key = make_key(person)
        key_map.setdefault(key, [])
        key_map[key].append(person)


def compare_persons(left, right):
    # If only one has .user, it's better
    if left.user is not None and right.user is None:
        return -1
    if right.user is not None and left.user is None:
        return 1

    # Otherwise the older the better
    return compare(left.created_at, right.created_at)