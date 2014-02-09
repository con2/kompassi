# encoding: utf-8

import json

from django.conf import settings

import requests
from requests_kerberos import HTTPKerberosAuth

DEFAULT_GROUPS = [
    'ipausers',
    'confluence-users',
    'jira-users',
    'crowd-users',
]


class IPAError(RuntimeError):
    pass

 
def add_user_to_group(username, groupname):
    raise NotImplemented()


def remove_user_from_group(username, groupname):
    raise NotImplemented()


def change_user_password(username, password):
    raise NotImplemented()


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
        "method": "user_add",
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