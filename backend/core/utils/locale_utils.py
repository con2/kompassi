from collections.abc import Mapping
from functools import cache
from typing import TypeVar

from babel import Locale
from django.conf import settings
from django.utils.translation import get_language

from graphql_api.language import SUPPORTED_LANGUAGES

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


@cache
def _get_babel_locale(lang):
    return Locale.parse(lang)


def get_current_locale():
    return _get_babel_locale(get_language() or DEFAULT_LANGUAGE)


T = TypeVar("T")


def get_message_in_language(
    messages: Mapping[str, T | None],
    lang: str | None = None,
) -> T | None:
    """
    Given a HStoreField, JSONField or a plain dict, assume keys are language codes
    and return the value for the current language.
    If the current language is not available, return the value for the default language.
    If the default language is not available, return the first value.

    Note that all three are considered to mean "no value in the specified language":
    - empty string
    - None/NULL
    - missing key

    Background: We used to use django-localized-fields for this, but it's a rather complex
    library for such a simple task. It also forces psqlextra as the database engine.
    So we yote them both and opted to use plain HStore/JSONFields instead.
    """
    if lang is None:
        lang = get_language()

    if found := messages.get(lang):
        return found

    for language in SUPPORTED_LANGUAGES:
        if found := messages.get(language.code):
            return found

    return next(iter(messages.values()), None)
