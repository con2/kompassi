# encoding: utf-8

from itertools import groupby
from random import randint
import re

from django import forms
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError
from django.utils.http import urlencode

from dateutil.tz import tzlocal


CHARACTER_CLASSES = [re.compile(r) for r in [
    r'.*[a-z]',
    r'.*[A-Z]',
    r'.*[0-9]',
    r'.*[^a-zA-Z0-9]',
]]


def check_password_strength(
    password,
    min_length=settings.KOMPASSI_PASSWORD_MIN_LENGTH,
    min_classes=settings.KOMPASSI_PASSWORD_MIN_CLASSES
):
    if min_length and len(password) < min_length:
        raise ValidationError(
            u'Salasanan tulee olla vähintään {0} merkkiä pitkä.'.format(min_length)
        )

    if min_classes:
        class_score = 0
        for class_re in CHARACTER_CLASSES:
            if class_re.match(password):
                class_score += 1

        if class_score < min_classes:
            raise ValidationError(
                u'Salasanassa tulee olla vähintään {0} seuraavista: pieni kirjain, iso '
                u'kirjain, numero, erikoismerkit. Ääkköset lasketaan erikoismerkeiksi'
                .format(min_classes)
            )


def give_all_app_perms_to_group(app_label, group):
    for ctype in ContentType.objects.filter(app_label=app_label):
        for perm in ctype.permission_set.all():
            perm.group_set.add(group)


def ensure_user_is_member_of_group(user, group, group_membership=True):
    if not group_membership:
        return ensure_user_is_not_member_of_group(user, group)

    if type(user) is not User:
        user = user.user

    group.user_set.add(user)

    if 'external_auth' in settings.INSTALLED_APPS:
        from external_auth.utils import add_user_to_group
        add_user_to_group(user, group)


def ensure_user_is_not_member_of_group(user, group):
    if type(user) is not User:
        user = user.user

    group.user_set.remove(user)

    if 'external_auth' in settings.INSTALLED_APPS:
        from external_auth.utils import remove_user_from_group
        remove_user_from_group(user, group)


def ensure_group_exists(group_name):
    if 'external_auth' in settings.INSTALLED_APPS:
        from external_auth.utils import ensure_group_exists as ea_ensure_group_exists
        ea_ensure_group_exists(group_name)

    return Group.objects.get_or_create(name=group_name)


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
    for key, value in attrs.iteritems():
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

    for key, value in kwargs.iteritems():
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
