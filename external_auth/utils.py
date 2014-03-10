# encoding: utf-8

from random import randint

import re
from django.conf import settings
from django.forms import ValidationError

from . import ipa


def create_temporary_password():
    return "".join(chr(randint(ord('0'), ord('z'))) for _ in range(64))


def get_user_dn(uid):
    return "uid={uid},{branch}".format(
        uid=uid,
        branch=settings.TURSKA_LDAP_USERS
    )


def create_user(user, password):
    temporary_password = create_temporary_password()

    ipa.create_user(
        username=user.username,
        first_name=user.first_name,
        surname=user.last_name,
        password=temporary_password,
    )

    for group_name in settings.TURSKA_NEW_USER_INITIAL_GROUPS:
        ipa.add_user_to_group(user.username, group_name)

    ipa.change_user_password(
        dn=get_user_dn(user.username),
        old_password=temporary_password,
        new_password=password,
    )


def change_current_user_password(request, old_password, new_password):
    ipa.change_user_password(
        dn=request.user.ldap_user.dn,
        old_password=old_password,
        new_password=new_password
    )


def add_user_to_group(user, group):
    ipa.add_user_to_group(user.username, group.name)


def reset_user_password(user, new_password):
    temporary_password = create_temporary_password()

    ipa.admin_set_user_password(user.username, temporary_password)
    ipa.change_user_password(
        dn=get_user_dn(user.username),
        old_password=temporary_password,
        new_password=new_password
    )
