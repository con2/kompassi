# encoding: utf-8

import re
from collections import namedtuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.forms import ValidationError

from access.utils import generate_machine_password

from .ipa import IPASession, IPAError


JustEnoughUser = namedtuple('JustEnoughUser', 'username first_name last_name email')
JustEnoughUser.__doc__ = """
    JustEnoughUser can be passed to most IPA functions instead of an actual User if one is not available at
    the time of the call of create_user.
"""


def create_user(user, password):
    assert isinstance(user, get_user_model()) or isinstance(user, JustEnoughUser)

    temporary_password = generate_machine_password()

    with IPASession.get_admin_session() as admin_session:
        admin_session.create_user(
            username=user.username,
            first_name=user.first_name,
            surname=user.last_name,
            email=user.email,
            password=temporary_password,
        )

        for group_name in settings.KOMPASSI_NEW_USER_INITIAL_GROUPS:
            admin_session.add_user_to_group(user.username, group_name)

    with IPASession(user.username, temporary_password, login=False) as user_session:
        user_session.change_own_password(password)


def update_user(user, password):
    assert isinstance(user, get_user_model()) or isinstance(user, JustEnoughUser)

    with IPASession.get_admin_session() as admin_session:
        admin_session.update_user(user.username,
            first_name=user.first_name,
            surname=user.last_name,
            email=user.email,
        )


def change_user_password(user, old_password, new_password):
    with IPASession(user.username, old_password) as user_session:
        user_session.change_own_password(new_password)


def ensure_user_group_membership(user, groups_to_add=[], groups_to_remove=[]):
    username = user if isinstance(user, basestring) else user.username
    groups_to_add = [group if isinstance(group, basestring) else group.name for group in groups_to_add]
    groups_to_remove = [group if isinstance(group, basestring) else group.name for group in groups_to_remove]

    with IPASession.get_admin_session() as admin_session:
        for group_name in groups_to_add:
            admin_session.add_user_to_group(username, group_name)

        for group_name in groups_to_remove:
            admin_session.remove_user_from_group(username, group_name)


def reset_user_password(user, new_password):
    temporary_password = generate_machine_password()

    with IPASession.get_admin_session() as admin_session:
        admin_session.change_password_for_another_user(user.username, temporary_password)

    with IPASession(user.username, temporary_password) as user_session:
        user_session.change_own_password(new_password)


def ensure_groups_exist(groups):
    groups = [group if isinstance(group, basestring) else group.name for group in groups]

    with IPASession.get_admin_session() as admin_session:
        for group_name in groups:
            admin_session.create_group(group_name)


def set_user_attrs_from_ipa_user_info(user, user_info):
    groups = set()
    groups.update(user_info['memberof_group'])
    groups.update(user_info['memberofindirect_group'])

    user.first_name = user_info['givenname'][0]
    user.last_name = user_info['sn'][0]
    user.is_active = settings.KOMPASSI_USERS_GROUP in groups
    user.is_staff = settings.KOMPASSI_STAFF_GROUP in groups
    user.is_superuser = settings.KOMPASSI_SUPERUSERS_GROUP in groups
    user.groups = [Group.objects.get_or_create(name=group_name)[0] for group_name in groups]

    return user


def sync_user_info(user):
    with IPASession.get_admin_session() as admin_session:
        user_info = admin_session.get_user_info(user.username)

    set_user_attrs_from_ipa_user_info(user, user_info)
    user.save()