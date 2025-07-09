from datetime import datetime, tzinfo
from typing import Protocol

from core.utils.locale_utils import get_message_in_language

from .language import DEFAULT_LANGUAGE, getattr_message_in_language


def resolve_localized_field(field_name: str):
    """
    Given a HStoreField, JSONField or a plain dict, assume keys are language codes
    and return a function that returns the value for the current language.
    If the current language is not available, return the value for the default language.
    If the default language is not available, return the first value.
    Field name is required to be provided because info.field_name is in camelCase.
    """

    def _resolve(parent, info, lang: str = DEFAULT_LANGUAGE) -> str:
        messages = getattr(parent, field_name)
        return get_message_in_language(messages, lang) or ""

    return _resolve


def resolve_localized_field_getattr(field_name_prefix: str):
    """
    Given a field name prefix, assume localized values are stored in fields with that prefix
    and the language code as a suffix, and return a function that returns the value for the current language.
    If the current language is not available, return the value for the default language.
    If the default language is not available, return the first value.
    Field name is required to be provided because info.field_name is in camelCase.
    """

    def _resolve(parent, info, lang: str | None = None) -> str:
        return getattr_message_in_language(parent, field_name_prefix, lang or DEFAULT_LANGUAGE)

    return _resolve


class HasTimezone(Protocol):
    timezone: tzinfo


def resolve_local_datetime_field(field_name: str):
    """
    Given a DateTimeField, return a function that returns the value in the local timezone.
    """

    def _resolve(parent: HasTimezone, info) -> datetime:
        dt = getattr(parent, field_name)
        return dt.astimezone(parent.timezone)

    return _resolve


def resolve_unix_seconds_field(field_name: str):
    def _resolve(parent, info) -> int:
        dt = getattr(parent, field_name)
        return int(dt.timestamp())

    return _resolve
