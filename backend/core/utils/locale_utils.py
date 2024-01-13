from functools import cache

from babel import Locale
from django.conf import settings
from django.utils.translation import get_language


@cache
def _get_babel_locale(lang):
    return Locale.parse(lang)


def get_current_locale():
    return _get_babel_locale(get_language() or settings.LANGUAGE_CODE)
