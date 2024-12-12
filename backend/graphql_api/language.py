from dataclasses import dataclass
from functools import cache, cached_property
from typing import Annotated


# TODO enumify
@dataclass
class Language:
    code: str
    name_fi: str
    name_en: str
    name_sv: str

    @cached_property
    def name_django(self):
        from django.utils.translation import gettext_lazy

        return gettext_lazy(self.name_en)


# NOTE: This must have same languages as supportedLanguages in frontend
# NOTE: The order of SUPPORTED_LANGUAGES defines the order resolve_localized_field will try to resolve the field
# NOTE: If you add a language, grep for "NOTE SUPPORTED_LANGUAGES" - some models have fields for each language
SUPPORTED_LANGUAGES = [
    Language("en", "englanti", "English", "engelska"),
    Language("fi", "suomi", "Finnish", "finska"),
    Language("sv", "ruotsi", "Swedish", "svenska"),
]
SUPPORTED_LANGUAGE_CODES = [lang.code for lang in SUPPORTED_LANGUAGES]


SupportedLanguageCode = Annotated[str, "SupportedLanguageCode"]


def to_supported_language(code: str) -> SupportedLanguageCode:
    if code not in SUPPORTED_LANGUAGE_CODES:
        return DEFAULT_LANGUAGE
    return code


# NOTE: This differs from settings.LANGUAGES in that these are offered in v2, settings.LANGUAGES in v1
@cache
def get_language_choices():
    return [(lang.code, lang.name_django) for lang in SUPPORTED_LANGUAGES]


# NOTE: sync with kompassi.settings.LANGUAGE_CODE
DEFAULT_LANGUAGE: SupportedLanguageCode = "en"
