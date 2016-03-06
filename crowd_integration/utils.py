# encoding: utf-8

from __future__ import unicode_literals

import json
import logging
import sys
from datetime import datetime

from django.conf import settings

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth


logger = logging.getLogger('kompassi')


AUTH = HTTPBasicAuth(
    settings.KOMPASSI_CROWD_APPLICATION_NAME,
    settings.KOMPASSI_CROWD_APPLICATION_PASSWORD,
)

HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}



class CrowdError(RuntimeError):
    pass


def crowd_request(method, url, params={}, body=None, ignore_status_codes=[]):
    url = '{base_url}{url}'.format(base_url=settings.KOMPASSI_CROWD_BASE_URL, url=url)

    response = requests.request(
        method=method,
        url=url,
        auth=AUTH,
        data=json.dumps(body) if body else None,
        headers=HEADERS,
        params=params,
    )

    if response.status_code in ignore_status_codes:
        return

    try:
        response.raise_for_status()
    except HTTPError as e:
        logger.exception(response.text)
        raise CrowdError(e)


def user_to_crowd(user, password=None):
    user_doc = {
        'name': user.username,
        'first-name': user.first_name,
        'last-name': user.last_name,
        'email': user.email,
        'active': True,
    }

    if password is not None:
        user_doc['password'] = {'value': password}

    return user_doc


def change_password(user, password):
    return crowd_request(
        'PUT',
        '/user/password',
        {'username': user.username},
        {'value': password},
    )


def ensure_group_exists(group_name):
    body = {
        "name": group_name,
        "type": "GROUP",
        "active": True
    }

    return crowd_request(
        'POST',
        '/group',
        {},
        body,
        ignore_status_codes=[400,],
    )


def ensure_user_group_membership(user, group_name, should_belong_to_group=True):
    if should_belong_to_group:
        ensure_user_is_member_of_group(user, group_name)
    else:
        ensure_user_is_not_member_of_group(user, group_name)


def ensure_user_is_member_of_group(user, group_name):
    return crowd_request(
        'POST',
        '/user/group/direct',
        {'username': user.username},
        {'name': group_name},
        ignore_status_codes=[409,]
    )


def ensure_user_is_not_member_of_group(user, group_name):
    return crowd_request(
        'DELETE',
        '/user/group/direct',
        {'username': user.username, 'groupname': group_name},
        ignore_status_codes=[404,]
    )


def create_user(user, password):
    return crowd_request(
        'POST',
        '/user',
        {},
        user_to_crowd(user, password)
    )


def update_user(user):
    return crowd_request(
        'PUT',
        '/user',
        {'username': user.username},
        user_to_crowd(user)
    )