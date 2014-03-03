# encoding: utf-8

from random import randint

import re
from django.conf import settings
from django.forms import ValidationError

from . import ipa


def create_user(user, password):
    temporary_password = "".join(chr(randint(ord('0'), ord('z'))) for _ in range(64))

    ipa.create_user(
        username=user.username,
        first_name=user.first_name,
        surname=user.last_name,
        password=temporary_password,
    )

    for group_name in settings.TURSKA_NEW_USER_INITIAL_GROUPS:
        ipa.add_user_to_group(user.username, group_name)

    dn = 'uid={0},{1}'.format(user.username, settings.TURSKA_LDAP_USERS)

    ipa.change_user_password(
        dn=dn,
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

