import re
from random import randint

from kompassi.core.utils import groups_of_n

EMAILIFY_CHAR_MAP = {
    " ": ".",
    ".": ".",
    "_": "-",
    "à": "a",
    "á": "a",
    "ä": "a",
    "å": "a",
    "è": "e",
    "é": "e",
    "ë": "e",
    "ö": "o",
    "ü": "u",
}
EMAILIFY_MULTIDASH_RE = re.compile(r"-+", re.UNICODE)
EMAILIFY_FORBANNAD_RE = re.compile(r"[^a-z0-9-\.]", re.UNICODE)
EMAILIFY_MULTIDOT_RE = re.compile(r"\.+", re.UNICODE)


def emailify(ustr):
    """
    >>> emailify("Bjärtil Ala-Ruuskanen")
    'bjartil.ala-ruuskanen'
    """
    ustr = ustr.lower()
    ustr = "".join(EMAILIFY_CHAR_MAP.get(c, c) for c in ustr)
    ustr = EMAILIFY_FORBANNAD_RE.sub("", ustr)
    ustr = EMAILIFY_MULTIDOT_RE.sub(".", ustr)
    ustr = EMAILIFY_MULTIDASH_RE.sub("-", ustr)
    ustr = ustr.removeprefix(".").removesuffix(".")
    return ustr  # noqa: RET504


PASSWORD_ALPHABET = "bcdfghjklmnpqrstvwxz0123456789"


def generate_machine_password(alphabet=PASSWORD_ALPHABET, num_chars=20, group_len=4):
    len_alphabet = len(PASSWORD_ALPHABET)
    chars = [alphabet[randint(0, len_alphabet - 1)] for _ in range(num_chars)]
    return "-".join("".join(part) for part in groups_of_n(chars, group_len))
