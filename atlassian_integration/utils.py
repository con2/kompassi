import json
import logging
import sys
from datetime import datetime

from django.conf import settings

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth


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


def crowd_login(username, password=None, request=None):
    """
    Establishes a Crowd SSO session for the specified user. If a password is specified, it is fed
    to Crowd and Crowd will perform authentication as well. If no password is specified, Crowd is
    instructed not to validate the password.

    If the login originates from the network, pass in request or remote_addr as a validation
    factor for Crowd.

    Returns a dict that can be fed as kwargs to HttpResponse.set_cookie.

    NB. We are using Crowd, Confluence and Kompassi behind an nginx proxy. If you are not, YMMV.
    """

    validation_factors = []

    for vf_name, vf_func in settings.KOMPASSI_CROWD_VALIDATION_FACTORS.iteritems():
        validation_factors.append(dict(
            name=vf_name,
            value=vf_func(request),
        ))

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
            'validationFactors': validation_factors
        },
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    log.debug(
        u'Processing Crowd login attempt {with_password} for {username} validation factors: {validation_factors}'
        .format(
            username=username,
            validation_factors=validation_factors,
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