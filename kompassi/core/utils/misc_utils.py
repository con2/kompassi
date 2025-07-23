import logging
from itertools import groupby
from random import randint

from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from ipware import get_client_ip

logger = logging.getLogger(__name__)


def give_all_app_perms_to_group(app_label, group):
    for ctype in ContentType.objects.filter(app_label=app_label):
        for perm in ctype.permission_set.all():  # type: ignore
            perm.group_set.add(group)  # type: ignore


def ensure_user_group_membership(user, groups_to_add=None, groups_to_remove=None):
    """
    Deprecated. Use ensure_user_is_member_of_group(user, group_or_name, True) # or False.

    This calling convention was due to IPA having considerable per-call overhead
    but being able to operate on multiple groups per call.
    """

    if groups_to_remove is None:
        groups_to_remove = []
    if groups_to_add is None:
        groups_to_add = []
    if not isinstance(user, User):
        user = user.user

    for group in groups_to_add:
        group.user_set.add(user)

    for group in groups_to_remove:
        group.user_set.remove(user)


def ensure_user_is_member_of_group(user, group, should_belong_to_group=True):
    if isinstance(group, str):
        group = Group.objects.get(name=group)
    elif isinstance(group, Group):
        pass
    else:
        group = group.group

    if should_belong_to_group:
        group.user_set.add(user)  # type: ignore
    else:
        group.user_set.remove(user)  # type: ignore


def ensure_groups_exist(group_names):
    return [Group.objects.get_or_create(name=group_name)[0] for group_name in group_names]


REMAP_MODULES = {
    "events.hitpoint2017": "zombies.hitpoint2017",
}


def get_code(path: str):
    """
    Given "core.utils.misc_utils:get_code", imports the module "core.utils.misc_utils" and returns
    "get_code" from it.
    """
    from importlib import import_module

    module_name, member_name = path.split(":")
    module_name = REMAP_MODULES.get(module_name, module_name)

    module = import_module(module_name)
    return getattr(module, member_name)


def set_attrs(obj, **attrs):
    for key, value in attrs.items():
        setattr(obj, key, value)

    return obj


def set_defaults(obj, **attrs):
    for key, value in attrs.items():
        if getattr(obj, key, None) is None:
            setattr(obj, key, value)

    return obj


def pick_attrs(obj, *attr_names, **extra_attrs):
    return dict(((attr_name, getattr(obj, attr_name)) for attr_name in attr_names), **extra_attrs)


def groups_of_n(iterable, n):
    cur_group = []
    for item in iterable:
        cur_group.append(item)
        if len(cur_group) == n:
            yield cur_group
            cur_group = []

    if cur_group:
        yield cur_group


def groupby_strict(*args, **kwargs):
    return [(key, list(values)) for (key, values) in groupby(*args, **kwargs)]


def create_temporary_password():
    return "".join(chr(randint(ord("0"), ord("z"))) for _ in range(64))


def mutate_query_params(request, mutations):
    """
    Return a mutated version of the query string of the request.

    The values of the `mutations` dict are interpreted thus:

    * `None`, `False`: Remove the key.
    * Any other value: Replace with this value.

    :param request: A HTTP request.
    :type request: django.http.HttpRequest
    :param mutations: A mutation dict.
    :type mutations: dict[str, object]
    :return: query string
    """

    new_qs = request.GET.copy()
    for key, value in mutations.items():
        if value in (None, False):
            new_qs.pop(key, None)
        else:
            new_qs[key] = value
    return new_qs.urlencode()


class class_property:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


def omit_keys(mapping, *keys_to_omit, **keys_to_set):
    return dict(((key, value) for (key, value) in mapping.items() if key not in keys_to_omit), **keys_to_set)


def get_ip(request):
    """
    Django-ipware 2.x compatibility wrapper for django-ipware 3.x
    """
    client_ip, is_routable = get_client_ip(request)
    return client_ip
