# encoding: utf-8

import json

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden


def initialize_form(FormClass, request, *args, **kwargs):
    if request.method == 'POST':
        return FormClass(request.POST, *args, **kwargs)
    else:
        return FormClass(*args, **kwargs)


def indented_without_label(input):
    return Div(Div(input, css_class='controls col-md-offset-3 col-md-9'), css_class='form-group')


def horizontal_form_helper():
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-5'
    return helper


class DateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            widget=forms.DateInput(format='%d.%m.%Y'),
            input_formats=(
                '%d.%m.%Y',
                '%Y-%m-%d'
            ),
            help_text='Muoto: 24.2.1994',
        )
        my_kwargs = dict(defaults, **kwargs)
        super(DateField, self).__init__(*args, **my_kwargs)


validate_slug = RegexValidator(
    regex=r'[a-z0-9-]+',
    message=u'Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.'
)


class SlugField(models.CharField):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=31,
            unique=True,
            validators=[validate_slug],
            verbose_name=u'Tekninen nimi',
            help_text=u'Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja '
                u'merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi '
                u'muuttaa luomisen jälkeen.',
        )
        my_kwargs = dict(defaults, **kwargs)
        super(SlugField, self).__init__(*args, **my_kwargs)


def url(view_name, *args):
    return reverse(view_name, args=args)


def json_response(data, **kwargs):
    return HttpResponse(json.dumps(data), content_type='text/json', **kwargs)


def render_string(request, template_name, vars):
    return render_to_string(template_name, vars, context_instance=RequestContext(request))


def format_date(date):
    return date.strftime(settings.DATE_FORMAT_STRFTIME)


def format_datetime(datetime):
    return datetime.strftime(settings.DATETIME_FORMAT_STRFTIME)
