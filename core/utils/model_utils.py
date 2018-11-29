from datetime import datetime, timedelta
from functools import wraps
from itertools import groupby
from random import randint
import json
import sys
import re

import phonenumbers

from django import forms
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db import models, connection
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from dateutil.tz import tzlocal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden


validate_slug = RegexValidator(
    regex=r'[a-z0-9-]+',
    message='Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.'
)


SLUG_FIELD_PARAMS = dict(
    max_length=255,
    unique=True,
    validators=[validate_slug],
    verbose_name='Tekninen nimi',
    help_text='Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja '
        'merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi '
        'muuttaa luomisen jälkeen.',
)
NONUNIQUE_SLUG_FIELD_PARAMS = dict(SLUG_FIELD_PARAMS, unique=False)


SLUGIFY_CHAR_MAP = {
  ' ': '-',
  '.': '-',
  '_': '-',
  'à': 'a',
  'á': 'a',
  'ä': 'a',
  'å': 'a',
  'è': 'e',
  'é': 'e',
  'ë': 'e',
  'ö': 'o',
  'ü': '',
}
SLUGIFY_FORBANNAD_RE = re.compile(r'[^a-z0-9-]', re.UNICODE)
SLUGIFY_MULTIDASH_RE = re.compile(r'-+', re.UNICODE)


def slugify(ustr):
    ustr = ustr.lower()
    ustr = ''.join(SLUGIFY_CHAR_MAP.get(c, c) for c in ustr)
    ustr = SLUGIFY_FORBANNAD_RE.sub('', ustr)
    ustr = SLUGIFY_MULTIDASH_RE.sub('-', ustr)
    return ustr


def get_postgresql_version_num():
    if not 'postgresql' in settings.DATABASES['default']['ENGINE']:
        return 0

    with connection.cursor() as cursor:
        cursor.execute('SHOW server_version_num')
        return int(cursor.fetchone()[0])


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


def _get_next_or_previous(queryset, obj, field, is_next):
    if isinstance(queryset, models.Model):
        queryset = queryset.objects  # we cheat – manager instead of qs, but it works here so idk

    if not obj.pk:
        raise ValueError("get_next/get_previous cannot be used on unsaved objects.")

    op = 'gt' if is_next else 'lt'
    desc_minus = '' if is_next else '-'

    param = getattr(obj, field_name)
    q = Q(**{'%s__%s' % (field_name, op): param})
    q = q | Q(**{field_name: param, 'pk__%s' % op: obj.pk})
    qs = queryset.filter(q).order_by(f'{desc_minus}{field_name}', '{desc_minus}pk')

    try:
        return qs[0]
    except IndexError:
        raise obj.DoesNotExist("%s matching query does not exist." % obj.__class__._meta.object_name)


def get_next(queryset, obj, field):
    return _get_next_or_previous(queryset, obj, field, True)


def get_previous(queryset, obj, field):
    return _get_next_or_previous(queryset, obj, field, False)


def phone_number_validator(value, region=settings.KOMPASSI_PHONENUMBERS_DEFAULT_REGION):
    """
    Validate the phone number using Google's phonenumbers library.
    """
    exc = _('Invalid phone number.')

    try:
        phone_number = phonenumbers.parse(value, region)
    except phonenumbers.NumberParseException as e:
        raise ValidationError(exc)
    else:
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(exc)


def format_phone_number(
    value,
    region=settings.KOMPASSI_PHONENUMBERS_DEFAULT_REGION,
    format=settings.KOMPASSI_PHONENUMBERS_DEFAULT_FORMAT
):
    """
    Formats a phone number or throws phonenumbers.NumberParseException.
    """

    phone_number_format = getattr(phonenumbers.PhoneNumberFormat, format, format)
    phone_number = phonenumbers.parse(value, region)
    return phonenumbers.format_number(phone_number, phone_number_format)
