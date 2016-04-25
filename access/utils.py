# encoding: utf-8

from __future__ import unicode_literals

import re
from random import randint

from core.utils.model_utils import SLUGIFY_CHAR_MAP, SLUGIFY_MULTIDASH_RE
from core.utils import groups_of_n


EMAILIFY_DIFFERENCES_TO_SLUGIFY = {
    ' ': '.',
    '.': '.',
}
EMAILIFY_CHAR_MAP = dict(SLUGIFY_CHAR_MAP, **EMAILIFY_DIFFERENCES_TO_SLUGIFY)
EMAILIFY_FORBANNAD_RE = re.compile(r'[^a-z0-9-\.]', re.UNICODE)
EMAILIFY_MULTIDOT_RE = re.compile(r'\.+', re.UNICODE)


def emailify(ustr):
    ustr = ustr.lower()
    ustr = ''.join(EMAILIFY_CHAR_MAP.get(c, c) for c in ustr)
    ustr = EMAILIFY_FORBANNAD_RE.sub('', ustr)
    ustr = EMAILIFY_MULTIDOT_RE.sub('.', ustr)
    ustr = SLUGIFY_MULTIDASH_RE.sub('-', ustr)
    return ustr


PASSWORD_ALPHABET = 'bcdfghjklmnpqrstvwxz0123456789'

def generate_machine_password(alphabet=PASSWORD_ALPHABET, num_chars=20, group_len=4):
    len_alphabet = len(PASSWORD_ALPHABET)
    chars = [alphabet[randint(0, len_alphabet - 1)] for _ in range(num_chars)]
    return "-".join("".join(part) for part in groups_of_n(chars, group_len))