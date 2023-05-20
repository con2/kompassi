import re

import phonenumbers

from django.conf import settings
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


validate_slug = RegexValidator(
    regex=r"[a-z0-9-]+", message="Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja."
)


SLUG_FIELD_PARAMS = dict(
    max_length=255,
    unique=True,
    validators=[validate_slug],
    verbose_name="Tekninen nimi",
    help_text='Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja '
    "merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi "
    "muuttaa luomisen jälkeen.",
)
NONUNIQUE_SLUG_FIELD_PARAMS = dict(SLUG_FIELD_PARAMS, unique=False)


SLUGIFY_CHAR_MAP = {
    " ": "-",
    ".": "-",
    "_": "-",
    "à": "a",
    "á": "a",
    "ä": "a",
    "å": "a",
    "è": "e",
    "é": "e",
    "ë": "e",
    "ö": "o",
    "ü": "",
}
SLUGIFY_FORBANNAD_RE = re.compile(r"[^a-z0-9-]", re.UNICODE)
SLUGIFY_MULTIDASH_RE = re.compile(r"-+", re.UNICODE)


def slugify(ustr):
    ustr = ustr.lower()
    ustr = "".join(SLUGIFY_CHAR_MAP.get(c, c) for c in ustr)
    ustr = SLUGIFY_FORBANNAD_RE.sub("", ustr)
    ustr = SLUGIFY_MULTIDASH_RE.sub("-", ustr)
    return ustr


def get_previous_and_next(queryset, current):
    if not current.pk:
        return None, None

    # TODO inefficient, done using a list
    signups = list(queryset)

    previous_item = None
    candidate = None

    for next_item in signups + [None]:
        if candidate and candidate.pk == current.pk:
            return previous_item, next_item

        previous_item = candidate
        candidate = next_item

    return None, None


def phone_number_validator(value, region=settings.KOMPASSI_PHONENUMBERS_DEFAULT_REGION):
    """
    Validate the phone number using Google's phonenumbers library.
    """
    exc = _("Invalid phone number.")

    try:
        phone_number = phonenumbers.parse(value, region)
    except phonenumbers.NumberParseException as e:
        raise ValidationError(exc)
    else:
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(exc)


def format_phone_number(
    value: str,
    region: str = settings.KOMPASSI_PHONENUMBERS_DEFAULT_REGION,
    format: str = settings.KOMPASSI_PHONENUMBERS_DEFAULT_FORMAT,
):
    """
    Formats a phone number or throws phonenumbers.NumberParseException.
    """

    phone_number_format = getattr(phonenumbers.PhoneNumberFormat, format, format)
    phone_number = phonenumbers.parse(value, region)
    return phonenumbers.format_number(phone_number, phone_number_format)
