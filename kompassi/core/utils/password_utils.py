import logging
from hashlib import sha1

import requests
from django.core.cache import caches
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from requests.exceptions import ConnectionError, HTTPError, Timeout
from zxcvbn import zxcvbn

logger = logging.getLogger(__name__)


ZXCVBN_MINIMUM_SCORE = 3
HIBP_PREFIX_LENGTH = 5
HIBP_BASE_URL = "https://api.pwnedpasswords.com/range"
HIBP_CACHE_EXPIRY_SECONDS = 7 * 24 * 60 * 60
HIBP_TIMEOUT_SECONDS = 3

# TODO: api.pwnedpasswords.com down?
HIBP_ENABLED = True


def validate_password(password, user_inputs=None):
    """
    Two-pronged password validity check suitable for use as a Django form validator function:

    1. Offline check using the zxcvbn library expecting a minimum score
    2. Check against the HIBPv2 API for known compromised passwords (https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/).
    """
    if user_inputs is None:
        user_inputs = []
    result = zxcvbn(password, user_inputs=user_inputs)

    if ZXCVBN_MINIMUM_SCORE is not None and result["score"] < ZXCVBN_MINIMUM_SCORE:
        raise ValidationError(_("Password too weak. Please use a stronger password."))

    if HIBP_ENABLED and is_password_compromised(password):
        raise ValidationError(
            _(
                "We check passwords securely against a database of known leaked passwords. "
                "This password has been compromised in a known leak. "
                "Please use another password."
            )
        )


def is_password_compromised(password):
    """
    Securely checks if the supplied password is compromised using the HIBPv2 API.

    Only the five first hex digits of the SHA1 hash of the password are transmitted to the
    HIBPv2 server.

    Returns True if the password was known to be compromised, False if it was not and
    None if the check failed due to external reasons (in which case a warning is logged).

    https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/
    """
    password_hash = sha1(password.encode("UTF-8")).hexdigest().upper()
    hash_prefix, hash_suffix = password_hash[:HIBP_PREFIX_LENGTH], password_hash[HIBP_PREFIX_LENGTH:]

    try:
        page_str = get_hibp_page(hash_prefix)
    except Timeout:
        logger.exception(
            "is_password_compromised: HIBPv2 API timed out while trying to query for page %s",
            hash_prefix,
        )
        return None
    except HTTPError as e:
        logger.exception(
            "is_password_compromised: HIBPv2 API returned status %d while trying to query for page %s",
            e.response.status_code,
            hash_prefix,
        )
        return None
    except ConnectionError:
        logger.exception(
            "is_password_compromised: HIBPv2 API connection error while trying to query for page %s",
            hash_prefix,
        )
        return None

    try:
        hibp_page = parse_hibp_page(page_str)
    except (ValueError, IndexError, KeyError):
        logger.exception("is_password_compromised: Failed to parse HIBPv2 page %s", hash_prefix)
        return None

    return hibp_page.get(hash_suffix, 0) > 0


def get_hibp_page(hash_prefix):
    """
    Gets a range of password hashes from the HIBPv2 API.

    Input is the first five hex digits of the plain SHA1 hash of the password.

    Returns the raw response body from the API suitable for feeding into parse_hibp_page.
    """
    # TODO Use a cache decorator

    if len(hash_prefix) != HIBP_PREFIX_LENGTH:
        raise AssertionError("Hash prefix length mismatch")

    try:
        int(hash_prefix, 16)
    except ValueError:
        raise AssertionError("Hash prefix is not valid hex") from None

    hash_prefix = hash_prefix.upper()

    cache = caches["default"]
    cache_key = f"get_hibp_page:{hash_prefix}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    result = requests.get(f"{HIBP_BASE_URL}/{hash_prefix}", timeout=HIBP_TIMEOUT_SECONDS)
    result.raise_for_status()

    page_str = result.text

    cache.set(cache_key, page_str, HIBP_CACHE_EXPIRY_SECONDS)

    return page_str


def parse_hibp_page(page_str):
    """
    >>> parse_hibp_page('A8C4A624898B4221FC963986F9DC19CF42E:1\r\nAA18199A6DB91A7A4BB1C4B2A89068DAAFC:1\r\n')
    {'A8C4A624898B4221FC963986F9DC19CF42E': 1, 'AA18199A6DB91A7A4BB1C4B2A89068DAAFC': 1}
    """

    return {
        hash_suffix: int(frequency)
        for (hash_suffix, frequency) in (line.split(":", 1) for line in page_str.splitlines())
    }
