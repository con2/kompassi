from itertools import groupby
from random import randint
import re

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError


def give_all_app_perms_to_group(app_label, group):
    for ctype in ContentType.objects.filter(app_label=app_label):
        for perm in ctype.permission_set.all():
            perm.group_set.add(group)


def ensure_user_group_membership(user, groups_to_add=[], groups_to_remove=[]):
    """
    Deprecated. Use ensure_user_is_member_of_group(user, group_or_name, True) # or False.

    This calling convention was due to IPA having considerable per-call overhead
    but being able to operate on multiple groups per call.
    """

    if not isinstance(user, User):
        user = user.user

    for group in groups_to_add:
        group.user_set.add(user)

    for group in groups_to_remove:
        group.user_set.remove(user)

    if 'crowd_integration' in settings.INSTALLED_APPS:
        from crowd_integration.utils import ensure_user_group_membership as cr_ensure_user_group_membership

        for group in groups_to_add:
            cr_ensure_user_group_membership(user, group.name, True)

        for group in groups_to_remove:
            cr_ensure_user_group_membership(user, group.name, False)


def ensure_user_is_member_of_group(user, group, should_belong_to_group=True):
    if isinstance(group, str):
        group = Group.objects.get(name=group)
    elif isinstance(group, Group):
        pass
    else:
        group = group.group

    if should_belong_to_group:
        group.user_set.add(user)
    else:
        group.user_set.remove(user)

    if 'crowd_integration' in settings.INSTALLED_APPS:
        from crowd_integration.utils import ensure_user_group_membership as cr_ensure_user_group_membership
        cr_ensure_user_group_membership(user, group.name, should_belong_to_group)


def ensure_groups_exist(group_names):
    groups = [Group.objects.get_or_create(name=group_name)[0] for group_name in group_names]

    if 'crowd_integration' in settings.INSTALLED_APPS:
        from crowd_integration.utils import ensure_group_exists

        for group_name in group_names:
            ensure_group_exists(group_name)

    return groups


class AllowPasswordChangeWithoutOldPassword(object):
    pass


def change_user_password(user, new_password, old_password=AllowPasswordChangeWithoutOldPassword):
    user.set_password(new_password)
    user.save()

    if 'crowd_integration' in settings.INSTALLED_APPS:
        from crowd_integration.utils import change_user_password as cr_change_user_password
        cr_change_user_password(user, new_password)


def get_code(path):
    """
    Given "core.utils:get_code", imports the module "core.utils" and returns
    "get_code" from it.
    """
    from importlib import import_module
    module_name, member_name = path.split(':')
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


def simple_object_init(self, *args, **kwargs):
    """
    Want a simple class that has a number of attributes writable via assignment or
    keywords in initialization?

    class MySimpleClass(object):
        __slots__ = ['foo', 'bar']
        from core.utils import simple_object_init as __init__

    my_simple_objects = MySimpleClass(foo=5)
    """

    for key, value in zip(self.__slots__, args):
        setattr(self, key, value)

    for key, value in kwargs.items():
        setattr(self, key, value)


def simple_object_repr(self):
    return "{class_name}({property_list})".format(
        class_name=self.__class__.__name__,
        property_list=', '.join(
            "{key}={value}".format(key=slot, value=repr(getattr(self, slot)))
            for slot in self.__slots__
        )
    )


def pick_attrs(obj, *attr_names, **extra_attrs):
    return dict(
        ((attr_name, getattr(obj, attr_name)) for attr_name in attr_names),
        **extra_attrs
    )


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
    return "".join(chr(randint(ord('0'), ord('z'))) for _ in range(64))


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


class class_property(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


def omit_keys(mapping, *keys_to_omit, **keys_to_set):
    return dict(
        ((key, value) for (key, value) in mapping.items() if key not in keys_to_omit),
        **keys_to_set
    )
