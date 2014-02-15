# encoding: utf-8

from contextlib import contextmanager
import json

from django.conf import settings

import ldap
import requests
from requests_kerberos import HTTPKerberosAuth


@contextmanager
def ldap_session():
    try:
        l = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
        yield l
    finally:
        l.unbind_s()


class IPAError(RuntimeError):
    pass

 
def add_user_to_group(username, groupname):
    return json_rpc('group_add_member', [groupname], dict(user=[username]))


def remove_user_from_group(username, groupname):
    return json_rpc('group_remove_member', [groupname], dict(user=[username]))


def change_current_user_password(request, old_password, new_password):
    try:
        with ldap_session() as l:
            dn = request.user.ldap_user.dn
            l.simple_bind_s(dn, old_password)
            l.passwd_s(request.user.ldap_user.dn, old_password, new_password)
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
        "Referer": settings.CONDB_IPA_JSONRPC,
        "Content-Type": "application/json",
    }

    payload = {
        "params": params,
        "method": method_name,
        "id": 0,
    }

    response = requests.post(settings.CONDB_IPA_JSONRPC,
        auth=HTTPKerberosAuth(),
        data=json.dumps(payload),
        headers=headers,
        verify=settings.CONDB_IPA_CACERT_PATH,
    )

    result = response.json()

    error = result.get('error', None)
    if error:
        raise IPAError(error)

    print response.headers, response.content