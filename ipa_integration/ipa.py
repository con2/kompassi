# encoding: utf-8

import json
import logging

from django.conf import settings

import requests
from requests import Session
from requests.exceptions import HTTPError


logger = logging.getLogger('kompassi')

IPA_LOGIN_URL = '{ipa}/session/login_password'.format(ipa=settings.KOMPASSI_IPA)
IPA_JSONRPC_URL = '{ipa}/session/json'.format(ipa=settings.KOMPASSI_IPA)
IPA_OTHER_USER_PASSWORD_MAGICK = 'CHANGING_PASSWORD_FOR_ANOTHER_USER'
IPA_GROUP_ADD_ERROR_ALREADY_EXISTS = 4002
IPA_HEADERS = {
    'Connection': 'keep-alive',
    'Referer': settings.KOMPASSI_IPA,
}


class IPAError(RuntimeError):
    pass


class IPASession(object):
    # Public API
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = Session()
        self.session.headers = dict(IPA_HEADERS)

    def __enter__(self):
        self._login()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.close()

    def get_user_info(self, username=None):
        if username is None:
            username = self.username

        return self._json_rpc('user_show', username)

    def change_own_password(self, new_password):
        return self._json_rpc('passwd', self.username, new_password, self.password)

    def change_password_for_another_user(self, username, new_password):
        return self._json_rpc('passwd', username, new_password, IPA_OTHER_USER_PASSWORD_MAGICK)

    def add_user_to_group(self, username, groupname):
        return self._json_rpc('group_add_member', groupname, user=[username])

    def remove_user_from_group(self, username, groupname):
        return self._json_rpc('group_remove_member', groupname, user=[username])

    def create_user(self, username, first_name, surname, password):
        return self._json_rpc('user_add', username,
            givenname=first_name,
            sn=surname,
            userpassword=password,
        )

    def create_group(self, group_name):
        try:
            return self._json_rpc('group_add', group_name, description=group_name)
        except IPAError as e:
            try:
                error, = e.args
                code = error['code']
            except (KeyError, IndexError):
                # ipa connectivity error or something else, bad
                raise e
            else:
                if code == IPA_GROUP_ADD_ERROR_ALREADY_EXISTS:
                    # group already exists
                    # we are under "ensure exists" semantics so this is kosher
                    return None
                else:
                    # some other error
                    raise e

    # Internal implementation
    def _login(self):
        payload = {
            'user': self.username,
            'password': self.password,
        }

        response = self.session.post(IPA_LOGIN_URL,
            data=payload,
            verify=settings.KOMPASSI_IPA_CACERT_PATH,
        )

        try:
            response.raise_for_status()
        except HTTPError as e:
            logger.exception('IPA login failed: %s', response.content)
            raise IPAError(e)

        return response.cookies

    def _json_rpc(self, method_name, *args, **kwargs):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {
            "params": [args, kwargs],
            "method": method_name,
            "id": 0,
        }

        response = self.session.post(IPA_JSONRPC_URL,
            data=json.dumps(payload),
            headers=headers,
            verify=settings.KOMPASSI_IPA_CACERT_PATH,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError, e:
            logger.exception('IPA JSON-RPC call failed: %s', response.content)
            raise IPAError(e)

        result = response.json()

        error = result.get('error', None)
        if error:
            raise IPAError(error)

        return result

    @classmethod
    def get_admin_session(
        cls,
        username=settings.KOMPASSI_IPA_ADMIN_USERNAME,
        password=settings.KOMPASSI_IPA_ADMIN_PASSWORD
    ):
        if not hasattr(cls, '_admin_session'):
            cls._admin_session = IPASession(username, password)

        return cls._admin_session