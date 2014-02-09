# encoding: utf-8

from django.conf import settings

import requests
from requests_kerberos import HTTPKerberosAuth

DEFAULT_GROUPS = [
    'ipausers',
    'confluence-users',
    'jira-users',
    'crowd-users',
]

def add_user_to_group(username, groupname):
    raise NotImplemented()

def create_user(*args, **kwargs):
    headers = {
        "referer": settings.IPA_JSONRPC,
        "content-type": "application/json",
    }

    payload = {
      "params": [
        [
          "testitunk"
        ],
        {
          "sn": "Tunk",
          "givenname": "Testi",
        }
      ],
      "method": "user_add",
      "id": 0
    }

    response = requests.post(settings.IPA_JSONRPC,
        auth=HTTPKerberosAuth,
        data=json.dumps(paylad),
        headers=headers
    )
