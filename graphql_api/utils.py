from django.utils import translation
from django.conf import settings


DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


def resolve_localized_field(field_name: str):
    """
    Given a LocalizedCharField or similar, this will resolve into its value in the currently active language.
    Field name is required to be provided because info.field_name is in camelCase.
    """

    def _resolve(parent, info, lang: str = DEFAULT_LANGUAGE):
        with translation.override(lang):
            return getattr(parent, field_name).translate()

    return _resolve
