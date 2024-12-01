from dataclasses import dataclass
from typing import Any

from django.conf import settings
from django.utils.translation import gettext_lazy as _


@dataclass
class Language:
    code: str
    name_fi: str
    name_en: str
    name_sv: str
    name_django: Any


# NOTE: This must have same languages as supportedLanguages in frontend
# NOTE: The order of SUPPORTED_LANGUAGES defines the order resolve_localized_field will try to resolve the field
# NOTE: If you add a language, grep for "NOTE SUPPORTED_LANGUAGES" - some models have fields for each language
SUPPORTED_LANGUAGES = [
    Language("en", "englanti", "English", "engelska", _("English")),
    Language("fi", "suomi", "Finnish", "finska", _("Finnish")),
    Language("sv", "ruotsi", "Swedish", "svenska", _("Swedish")),
]
SUPPORTED_LANGUAGE_CODES = [lang.code for lang in SUPPORTED_LANGUAGES]

# NOTE: This differs from settings.LANGUAGES in that these are offered in v2, settings.LANGUAGES in v1
LANGUAGE_CHOICES = [(lang.code, lang.name_django) for lang in SUPPORTED_LANGUAGES]
DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE
