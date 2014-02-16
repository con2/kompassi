# encoding: utf-8

import re
from random import randint

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


CHARACTER_CLASSES = [re.compile(r) for r in [
    r'.*[a-z]',
    r'.*[A-Z]',
    r'.*[0-9]',
    r'.*[^a-zA-Z0-9]',
]]


def check_password_strength(
    password,
    min_length=settings.TURSKA_PASSWORD_MIN_LENGTH,
    min_classes=settings.TURSKA_PASSWORD_MIN_CLASSES
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