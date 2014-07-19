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


def crowd_application_auth():
    return HTTPBasicAuth(
        settings.KOMPASSI_CROWD_APPLICATION_NAME,
        settings.KOMPASSI_CROWD_APPLICATION_PASSWORD
    )


def crowd_session_url(token=None):
    base_url = settings.KOMPASSI_CROWD_SESSION_URL

    if token is not None:
        return "{base_url}/{token}".format(base_url=base_url, token=token) # TODO validate token?
    else:
        return base_url


def crowd_login(username, password=None, remote_addr=None, request=None):
    """
    Establishes a Crowd SSO session for the specified user. If a password is specified, it is fed
    to Crowd and Crowd will perform authentication as well. If no password is specified, Crowd is
    instructed not to validate the password.

    If the login originates from the network, pass in request or remote_addr as a validation
    factor for Crowd.

    Returns a dict that can be fed as kwargs to HttpResponse.set_cookie.
    """

    if remote_addr is not None and request is not None:
        raise TypeError("Only one of remote_addr and request may be passed")

    if request is not None:
        remote_addr = get_real_ip(request)
        log.debug('Crowd login IP resolved via get_real_ip: {remote_addr}'.format(remote_addr=remote_addr))

    if remote_addr is None:
        remote_addr = '127.0.0.1'
        log.warning(
            'Unable to resolve login IP for {username}. Falling back to {remote_addr}.'
            .format(username=username, remote_addr=remote_addr)
        )

    auth = crowd_application_auth()

    # https://developer.atlassian.com/display/CROWDDEV/JSON+Requests+and+Responses
    # https://developer.atlassian.com/display/CROWDDEV/Crowd+REST+Resources#CrowdRESTResources-CrowdSSOTokenResource

    params = dict()
    if password is None:
        params['validate-password'] = 'false'

    payload = {
        'username': username,
        'password': password,
        'validation-factors': {
            'validationFactors': [
                {
                    'name': 'remote_address',
                    'value': '127.0.0.1',
                },
                {
                    'name': 'X-Forwarded-For',
                    'value': remote_addr,
                },
            ],
        },
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    log.debug(
        u'Processing Crowd login attempt for {username} from {remote_addr} {with_password}'
        .format(
            username=username,
            remote_addr=remote_addr,
            with_password='with password' if password is not None else u'without password',
        )
    )

    try:
        response = requests.post(
            crowd_session_url(),
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
        log.error(u'Crowd authentication failed for {username}: {e}'.format(username=username, e=e))
        unused, unused, traceback = sys.exc_info()
        raise CrowdError, e, traceback

    log.debug(u'Crowd authentication succeeded for {username}'.format(username=username))

    return dict(
        settings.KOMPASSI_CROWD_COOKIE_ATTRS,
        value=token,
        expires=expires,
    )


def crowd_logout(request):
    token = request.COOKIES.get(settings.KOMPASSI_CROWD_COOKIE_ATTRS['key'])
    username = request.user.username

    if not token:
        log.warning(u'No Crowd cookie at logout for {username}'.format(username=username))
        return None

    auth = crowd_application_auth()

    try:
        response = requests.delete(
            crowd_session_url(token=token),
            auth=auth,
        )
    except Exception as e:
        log.error(u'Crowd logout failed for {username}: {e}'.format(username=username, e=e))
        # Fall through: Delete the cookie anyway.

    return dict(
        (key, settings.KOMPASSI_CROWD_COOKIE_ATTRS[key])
        for key in ('key', 'path', 'domain')
    )