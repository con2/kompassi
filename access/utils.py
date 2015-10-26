# encoding: utf-8

import re

from core.utils.model_utils import SLUGIFY_CHAR_MAP, SLUGIFY_MULTIDASH_RE


EMAILIFY_DIFFERENCES_TO_SLUGIFY = {
    u' ': u'.',
    u'.': u'.',
}
EMAILIFY_CHAR_MAP = dict(SLUGIFY_CHAR_MAP, **EMAILIFY_DIFFERENCES_TO_SLUGIFY)
EMAILIFY_FORBANNAD_RE = re.compile(ur'[^a-z0-9-\.]', re.UNICODE)
EMAILIFY_MULTIDOT_RE = re.compile(ur'\.+', re.UNICODE)


def emailify(ustr):
    ustr = ustr.lower()
    ustr = u''.join(EMAILIFY_CHAR_MAP.get(c, c) for c in ustr)
    ustr = EMAILIFY_FORBANNAD_RE.sub(u'', ustr)
    ustr = EMAILIFY_MULTIDOT_RE.sub(u'.', ustr)
    ustr = SLUGIFY_MULTIDASH_RE.sub(u'-', ustr)
    return ustr