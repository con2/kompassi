# encoding: utf-8

from functools import wraps
from urllib import urlencode
import json
import re

from django import forms
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.timezone import get_default_timezone
from django.template import RequestContext, defaultfilters
from django.template.loader import render_to_string

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden


def make_field_readonly(field):
    if type(field.widget) in [
        forms.widgets.CheckboxSelectMultiple,
        forms.widgets.CheckboxInput,
    ]:
        field.widget.attrs['disabled'] = True
    else:
        field.widget.attrs['readonly'] = True


def initialize_form(FormClass, request, **kwargs):
    if 'readonly' in kwargs:
        readonly = kwargs.pop('readonly')
    else:
        readonly = False

    if not readonly and request.method == 'POST':
        form = FormClass(request.POST, **kwargs)
    else:
        form = FormClass(**kwargs)

    if readonly:
        for field in form.fields.values():
            make_field_readonly(field)

    return form


def initialize_form_set(FormSetClass, request, **kwargs):
    if 'readonly' in kwargs:
        readonly = kwargs.pop('readonly')
    else:
        readonly = False

    if not readonly and request.method == 'POST':
        form_set = FormSetClass(request.POST, **kwargs)
    else:
        form_set = FormSetClass(**kwargs)

    if readonly:
        for form in form_set:
            for field in form.fields.values():
                make_field_readonly(field)

    return form_set


def indented_without_label(input, css_class='col-md-offset-3 col-md-9'):
    return Div(Div(input, css_class='controls {}'.format(css_class)), css_class='form-group')


def make_horizontal_form_helper(helper):
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-9'
    return helper


def horizontal_form_helper():
    return make_horizontal_form_helper(FormHelper())


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


SLUG_FIELD_PARAMS = dict(
    max_length=63,
    unique=True,
    validators=[validate_slug],
    verbose_name=u'Tekninen nimi',
    help_text=u'Tekninen nimi eli "slug" näkyy URL-osoitteissa. Sallittuja '
        u'merkkejä ovat pienet kirjaimet, numerot ja väliviiva. Teknistä nimeä ei voi '
        u'muuttaa luomisen jälkeen.',
)


def url(view_name, *args):
    return reverse(view_name, args=args)


def json_response(data, **kwargs):
    return HttpResponse(json.dumps(data), content_type='text/json', **kwargs)


def render_string(request, template_name, vars):
    return render_to_string(template_name, vars, context_instance=RequestContext(request))


def format_date(date):
    return defaultfilters.date(date, "SHORT_DATE_FORMAT")


def format_datetime(datetime):
    tz = get_default_timezone()
    return defaultfilters.date(datetime.astimezone(tz), "SHORT_DATETIME_FORMAT")


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
    min_length=settings.KOMPASSI_PASSWORD_MIN_LENGTH,
    min_classes=settings.KOMPASSI_PASSWORD_MIN_CLASSES
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


def page_wizard_init(request, pages):
    assert all(len(page) in [2, 3] for page in pages)

    steps = []
    all_related = set()

    for index, page in enumerate(pages):
        if len(page) == 2:
            name, title = page
            cur_related = []
        else:
            name, title, cur_related = page

        title = u"{}. {}".format(index + 1, title)

        cur_related = set(cur_related)
        cur_related.add(name)
        cur_related = list(i if i.startswith('/') else url(i) for i in cur_related)
        all_related.update(cur_related)

        steps.append((name, title, cur_related))

    request.session['core.utils.page_wizard.steps'] = steps
    request.session['core.utils.page_wizard.related'] = list(all_related)


def page_wizard_clear(request):
    if 'core.utils.page_wizard.steps' in request.session:
        # raise RuntimeError('WHO DARES CALL PAGE_WIZARD_CLEAR')
        del request.session['core.utils.page_wizard.steps']
        del request.session['core.utils.page_wizard.related']


def page_wizard_vars(request):
    next = get_next(request)

    if 'core.utils.page_wizard.steps' in request.session:
        page_wizard = []
        active = False

        for name, title, related in request.session['core.utils.page_wizard.steps']:
            if active:
                next = name if name.startswith('/') else reverse(name)

            active = request.path in related
            page_wizard.append((title, active))

        return dict(
            page_wizard=page_wizard,
            next=next,
        )
    else:
        return dict(next=next)


def give_all_app_perms_to_group(app_label, group):
    for ctype in ContentType.objects.filter(app_label=app_label):
        for perm in ctype.permission_set.all():
            perm.group_set.add(group)


def ensure_user_is_member_of_group(user, group):
    if type(user) is not User:
        user = user.user

    group.user_set.add(user)

    if 'external_auth' in settings.INSTALLED_APPS:
        from external_auth.utils import add_user_to_group
        add_user_to_group(user, group)


def ensure_user_is_not_member_of_group(user, group):
    if type(user) is not User:
        user = user.user

    group.user_set.remove(user)

    if 'external_auth' in settings.INSTALLED_APPS:
        from external_auth.utils import remove_user_from_group
        remove_user_from_group(user, group)
