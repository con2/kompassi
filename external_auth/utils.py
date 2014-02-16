# encoding: utf-8

from django.conf import settings

from . import ipa

def create_user(user, password):
    temporary_password = 'A very long 1-time temporary password'

    ipa.create_user(
        username=user.username,
        first_name=user.first_name,
        surname=user.last_name,
        password=temporary_password,
    )

    for group_name in settings.CONDB_NEW_USER_INITIAL_GROUPS:
        ipa.add_user_to_group(user.username, group_name)
    
    dn = 'uid=%s,%s' % (user.username, settings.CONDB_LDAP_USERS)
    
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