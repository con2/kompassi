# encoding: utf-8

import json
import re
from urllib import urlencode

from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import RequestContext
from django.template.loader import render_to_string

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden
from django.utils.timezone import get_default_timezone


def initialize_form(FormClass, request, *args, **kwargs):
    if request.method == 'POST':
        return FormClass(request.POST, *args, **kwargs)
    else:
        return FormClass(*args, **kwargs)


def multiform_validate(forms):
    return ["syntax"] if not all(
        i.is_valid() and (i.instance.target.available or i.cleaned_data["count"] == 0)
        for i in forms
    ) else []


def multiform_save(forms):
    return [i.save() for i in forms]


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
            max_length=63,
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
    return datetime.astimezone(get_default_timezone()).strftime(settings.DATETIME_FORMAT_STRFTIME)


def login_redirect(request, view='core_login_view'):
    path = reverse(view)
    query = urlencode(dict(next=request.path))
    return HttpResponseRedirect("{path}?{query}".format(**locals()))


def get_next(request, default='core_frontpage_view'):
    if request.method == 'GET':
        next = request.GET.get('next', None)
    elif request.method == 'POST':
        next = request.POST.get('next', None)
    else:
        raise NotImplemented(request.method)

    return next if next else default


def next_redirect(request, default='core_frontpage_view'):
    next = get_next(request, default)
    return redirect(next)


CHARACTER_CLASSES = [re.compile(r) for r in [
    r'.*[a-z]',
    r'.*[A-Z]',
    r'.*[0-9]',
    r'.*[^a-zA-Z0-9]',
]]


def check_password_strength(
    password,
    min_length=settings.TURSKA_PASSWORD_MIN_LENGTH,
    min_classes=settings.TURSKA_PASSWORD_MIN_CLASSES
):
    if min_length and len(password) < min_length:
        raise ValidationError(
            u'Salasanan tulee olla vähintään {0} merkkiä pitkä.'.format(min_length)
        )

    if min_classes:
        class_score = 0
        for class_re in CHARACTER_CLASSES:
            if class_re.match(password):
                class_score += 1

        if class_score < min_classes:
            raise ValidationError(
                u'Salasanassa tulee olla vähintään {0} seuraavista: pieni kirjain, iso '
                u'kirjain, numero, erikoismerkit. Ääkköset lasketaan erikoismerkeiksi'
                .format(min_classes)
            )
