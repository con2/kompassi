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

    with NamedTemporaryFile() as ccache_file:
        try:
            l = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
            auth = ldap.sasl.gssapi("")
            l.sasl_interactive_bind_s("", auth)
            yield l
        finally:
            l.unbind_s()


class IPAError(RuntimeError):
    pass


def add_user_to_group(username, groupname):
    return json_rpc('group_add_member', [groupname], dict(user=[username]))


def remove_user_from_group(username, groupname):
    return json_rpc('group_remove_member', [groupname], dict(user=[username]))


def change_user_password(dn, old_password, new_password):
    with ldap_session() as l:
        l.simple_bind_s(dn, old_password)
        l.passwd_s(dn, old_password, new_password)


def ldap_modify(dn, *modlist):
    try:
        with ldap_session() as l:
            l.modify_s(dn, modlist)
    except ldap.LDAPError, e:
        raise IPAError(e)


def create_user(username, first_name, surname, password):
    attrs = dict(
        givenname=first_name,
        sn=surname,
        userpassword=password,
    )

    return json_rpc('user_add', [username], attrs)


def json_rpc(method_name, *params):
    headers = {
        "Referer": settings.TURSKA_IPA_JSONRPC,
        "Content-Type": "application/json",
    }

    payload = {
        "params": params,
        "method": method_name,
        "id": 0,
    }

    response = requests.post(settings.TURSKA_IPA_JSONRPC,
        auth=HTTPKerberosAuth(),
        data=json.dumps(payload),
        headers=headers,
        verify=settings.TURSKA_IPA_CACERT_PATH,
    )

    try:
        response.raise_for_status()
    except HTTPError, e:
        raise IPAError(e)

    result = response.json()

    error = result.get('error', None)
    if error:
        raise IPAError(error)

    print response.headers, response.content


def reset_password_expiry(dn, username):
    ldap_modify(dn,
        (ldap.MOD_REPLACE, 'krbpasswordexpiration', '20170101000000Z'),
    )


def reset_user_password(user, new_password):
    raise NotImplemented()
