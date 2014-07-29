# encoding: utf-8

from contextlib import contextmanager
import json
from tempfile import NamedTemporaryFile

from django.conf import settings

import ldap
import ldap.sasl
import requests
from requests_kerberos import HTTPKerberosAuth


@contextmanager
def ldap_session():
    for key, value in settings.AUTH_LDAP_GLOBAL_OPTIONS.iteritems():
        ldap.set_option(key, value)

    try:
        l = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
        auth = ldap.sasl.gssapi("")
        l.sasl_interactive_bind_s("", auth)
        yield l
    except ldap.LDAPError, e:
        raise IPAError(e)
    finally:
        l.unbind_s()


def u(unicode_string):
    return unicode_string.encode('UTF-8')


class IPAError(RuntimeError):
    pass


def add_user_to_group(username, groupname):
    return json_rpc('group_add_member', groupname, user=[username])


def remove_user_from_group(username, groupname):
    return json_rpc('group_remove_member', groupname, user=[username])


def change_user_password(dn, old_password, new_password):
    with ldap_session() as l:
        l.simple_bind_s(dn, u(old_password))
        l.passwd_s(dn, u(old_password), u(new_password))


def ldap_modify(dn, *modlist):
    with ldap_session() as l:
        l.modify_s(dn, modlist)


def create_user(username, first_name, surname, password):
    return json_rpc('user_add', username,
        givenname=first_name,
        sn=surname,
        userpassword=password,
    )


def create_group(group_name):
    return json_rpc('group_add', group_name)


def json_rpc(method_name, *args, **kwargs):
    headers = {
        "Referer": settings.KOMPASSI_IPA_JSONRPC,
        "Content-Type": "application/json",
    }

    payload = {
        "params": [args, kwargs],
        "method": method_name,
        "id": 0,
    }

    response = requests.post(settings.KOMPASSI_IPA_JSONRPC,
        auth=HTTPKerberosAuth(),
        data=json.dumps(payload),
        headers=headers,
        verify=settings.KOMPASSI_IPA_CACERT_PATH,
    )

    try:
        response.raise_for_status()
    except requests.HTTPError, e:
        raise IPAError(e)

    result = response.json()

    error = result.get('error', None)
    if error:
        raise IPAError(error)

    return result


def admin_set_user_password(username, new_password):
    return json_rpc('user_mod', username,
        all=False,
        rights=False,
        userpassword=new_password,
        random=False,
        raw=False,
    )
