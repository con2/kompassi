# encoding: utf-8

import re
from django.conf import settings
from django.forms import ValidationError

from access.utils import generate_machine_password

from .ipa import IPASession, IPAError


def create_user(user, password):
    temporary_password = generate_machine_password()

    with IPASession.get_admin_session() as admin_session:
        admin_session.create_user(
            username=user.username,
            first_name=user.first_name,
            surname=user.last_name,
            password=temporary_password,
        )

        for group_name in settings.KOMPASSI_NEW_USER_INITIAL_GROUPS:
            admin_session.add_user_to_group(user.username, group_name)

    with IPASession(user.username, temporary_password) as user_session:
        user_session.change_own_password(temporary_password, password)


def change_current_user_password(request, old_password, new_password):
    with IPASession(request.user.username, old_password) as user_session:
        user_session.change_own_password(old_password, new_password)


def ensure_user_group_membership(user, groups_to_add=[], groups_to_remove=[]):
    username = user if isinstance(user, basestring) else user.username
    groups_to_add = [group if isinstance(group, basestring) else group.name for group in groups_to_add]
    groups_to_remove = [group if isinstance(group, basestring) else group.name for group in groups_to_remove]

    with IPASession.get_admin_session() as admin_session:
        for group_name in groups:
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