import json
import logging
import sys
from datetime import datetime

from django.conf import settings

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth
from ipware.ip import get_real_ip


log = logging.getLogger(__name__)


class CrowdError(RuntimeError):
    pass


def crowd_login(username, password=None, remote_addr=None, request=None):
    """
    Establishes a Crowd SSO session for the specified user. If a password is specified, it is fed
    to Crowd and Crowd will perform authentication as well. If no password is specified, Crowd is
    instructed not to validate the password.

    If the login originates from the network, pass in request or remote_addr as a validation
    factor for Crowd.
    """

    if remote_addr is not None and request is not None:
        raise TypeError("Only one of remote_addr and request may be passed")

    if request is not None:
        remote_addr = get_real_ip(request)

    if remote_addr is None:
        remote_addr = '127.0.0.1'

    auth = HTTPBasicAuth(
        settings.KOMPASSI_CROWD_APPLICATION_NAME,
        settings.KOMPASSI_CROWD_APPLICATION_PASSWORD
    )

    # https://developer.atlassian.com/display/CROWDDEV/JSON+Requests+and+Responses
    # https://developer.atlassian.com/display/CROWDDEV/Crowd+REST+Resources#CrowdRESTResources-CrowdSSOTokenResource

    params = dict()
    if password is None:
        params['validate-password'] = 'false'

    payload = {
        'username': username,
        'password': password,
        # 'validation-factors': {
        #     'validationFactors': [
        #         {
        #             'name': 'remote_addr',
        #             'value': remote_addr
        #         }
        #     ]
        # },
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    try:
        response = requests.post(
            settings.KOMPASSI_CROWD_SESSION_URL,
            auth=auth,
            data=json.dumps(payload),
            headers=headers,
            params=params,
        )

        response.raise_for_status()

        response_json = response.json()


        token = unicode(response_json['token'])
        expires = datetime.utcfromtimestamp(int(response_json['expiry-date']) / 1000.0)
    except Exception as e:
        unused, unused, traceback = sys.exc_info()
        raise CrowdError, e, traceback

    log.debug('Crowd authentication succeeded for {username}'.format(username=username))

    return dict(
        settings.KOMPASSI_CROWD_COOKIE_ATTRS,
        value=token,
        expires=expires,
    )
