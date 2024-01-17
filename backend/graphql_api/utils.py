from django.conf import settings

from core.utils.locale_utils import get_message_in_language

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


def resolve_localized_field(field_name: str):
    """
    Given a HStoreField, JSONField or a plain dict, assume keys are language codes
    and return a function that returns the value for the current language.
    If the current language is not available, return the value for the default language.
    If the default language is not available, return the first value.
    Field name is required to be provided because info.field_name is in camelCase.
    """

    def _resolve(parent, info, lang: str = DEFAULT_LANGUAGE):
        messages = getattr(parent, field_name)
        get_message_in_language(messages, lang)

    return _resolve
