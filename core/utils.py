# encoding: utf-8

from functools import wraps
from itertools import groupby
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
from django.utils.timezone import now
from django.template import RequestContext, defaultfilters
from django.template.loader import render_to_string

from dateutil.tz import tzlocal

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
NONUNIQUE_SLUG_FIELD_PARAMS = dict(SLUG_FIELD_PARAMS, unique=False)


def url(view_name, *args):
    return reverse(view_name, args=args)


def json_response(data, **kwargs):
    return HttpResponse(json.dumps(data), content_type='text/json', **kwargs)


def render_string(request, template_name, vars):
    return render_to_string(template_name, vars, context_instance=RequestContext(request))


def format_date(date):
    return defaultfilters.date(date, "SHORT_DATE_FORMAT")


def format_datetime(datetime):
    tz = tzlocal()
    return defaultfilters.date(datetime.astimezone(tz), "SHORT_DATETIME_FORMAT")


def format_date_range(start_date, end_date):
    # XXX Finnish-specific

    if start_date.year == end_date.year:
        if start_date.month == end_date.month:
            if start_date.day == end_date.day:
                # Y, M, D match
                return start_date.strftime('%-d.%-m.%Y')
            else:
                # Y, M match, D differ
                return u"{start_date}–{end_date}".format(
                    start_date=start_date.strftime('%-d.'),
                    end_date=end_date.strftime('%-d.%-m.%Y'),
                )
        else:
            # Y match, M, D differ
            return u"{start_date}–{end_date}".format(
                start_date=start_date.strftime('%-d.%-m.'),
                end_date=end_date.strftime('%-d.%-m.%Y')
            )
    else:
        # Y, M, D differ
        return u"{start_date}–{end_date}".format(
            start_date=start_date.strftime('%-d.%-m.%Y'),
            end_date=end_date.strftime('%-d.%-m.%Y'),
        )


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


def ensure_user_is_member_of_group(user, group, group_membership=True):
    if not group_membership:
        return ensure_user_is_not_member_of_group(user, group)

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


def ensure_group_exists(group_name):
    if 'external_auth' in settings.INSTALLED_APPS:
        from external_auth.utils import ensure_group_exists as ea_ensure_group_exists
        ea_ensure_group_exists(group_name)

    return Group.objects.get_or_create(name=group_name)


def get_code(path):
    """
    Given "core.utils:get_code", imports the module "core.utils" and returns
    "get_code" from it.
    """
    from importlib import import_module
    module_name, member_name = path.split(':')
    module = import_module(module_name)
    return getattr(module, member_name)


def code_property(code_field_name):
    """
    class MyModel(models.Model):
        do_something_code = models.CharField(max_length=255)
        do_something = code_property("do_something_code")
    """

    def _get(self):
        from core.utils import get_code
        return get_code(getattr(self, code_field_name))

    return property(_get)


def is_within_period(period_start, period_end, t=None):
    if t is None:
        from django.utils.timezone import now
        t = now()

    return period_start and period_start <= t and \
        not (period_end and period_end <= t)


def set_attrs(obj, **attrs):
    for key, value in attrs.iteritems():
        setattr(obj, key, value)

    return obj


def alias_property(name):
    def _get(self):
        return getattr(self, name)

    def _set(self, value):
        setattr(self, name, value)

    def _del(self):
        delattr(self, name)

    return property(_get, _set, _del)


def time_bool_property(name):
    """
    Uses a DateTimeField to implement a boolean property that records when the value was first set
    to True. This is best illustrated by the following table of transitions:

    False -> False: Nothing happens
    False -> True:  Underlying attribute is set to the current time
    True  -> False: Underlying attribute is set to None
    True ->  True:  Nothing happens
    """

    def _get(self):
        return getattr(self, name) is not None

    def _set(self, value):
        if bool(getattr(self, name)) == bool(value):
            pass
        else:
            setattr(self, name, now() if value else None)

    return property(_get, _set)


SLUGIFY_CHAR_MAP = {
  u'ä': u'a',
  u'å': u'a',
  u'ö': u'o',
  u'ü': u'u',
  u' ': u'-',
  u'_': u'-',
  u'.': u'-',
}
SLUGIFY_FORBANNAD_RE = re.compile(ur'[^a-z0-9-]', re.UNICODE)
SLUGIFY_MULTIDASH_RE = re.compile(ur'-+', re.UNICODE)


def slugify(ustr):
    ustr = ustr.lower()
    ustr = u''.join(SLUGIFY_CHAR_MAP.get(c, c) for c in ustr)
    ustr = SLUGIFY_FORBANNAD_RE.sub(u'', ustr)
    ustr = SLUGIFY_MULTIDASH_RE.sub(u'-', ustr)
    return ustr


def simple_object_init(self, **kwargs):
    """
    Want a simple class that has a number of attributes writable via assignment or
    keywords in initialization?

    class MySimpleClass(object):
        __slots__ = ['foo', 'bar']
        from core.utils import simple_object_init as __init__

    my_simple_objects = MySimpleClass(foo=5)
    """

    for key, value in kwargs.iteritems():
        setattr(self, key, value)


def simple_object_repr(self):
    return "{class_name}({property_list})".format(
        class_name=self.__class__.__name__,
        property_list=', '.join(
            "{key}={value}".format(key=slot, value=repr(getattr(self, slot)))
            for slot in self.__slots__
        )
    )


def event_meta_property(app_label, code_path):
    if app_label not in settings.INSTALLED_APPS:
        return property(lambda self: None)

    def _get(self):
        # NOTE moving get_code invocation outside _get would create a circular import
        EventMetaClass = get_code(code_path)

        try:
            return EventMetaClass.objects.get(event=self)
        except EventMetaClass.DoesNotExist:
            return None

    return property(_get)


def pick_attrs(obj, *attr_names, **extra_attrs):
    return dict(
        (attr_name, getattr(obj, attr_name))
        for attr_name in attr_names,
        **extra_attrs
    )


def groups_of_n(iterable, n):
    cur_group = []
    for item in iterable:
        cur_group.append(item)
        if len(cur_group) == n:
            yield cur_group
            cur_group = []

    if cur_group:
        yield cur_group


def groupby_strict(*args, **kwargs):
    return [(key, list(values)) for (key, values) in groupby(*args, **kwargs)]
