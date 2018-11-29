# encoding: utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div


def make_field_readonly(field):
    if type(field.widget) in [
        forms.widgets.CheckboxSelectMultiple,
        forms.widgets.CheckboxInput,
    ]:
        field.widget.attrs['disabled'] = True
    else:
        field.widget.attrs['readonly'] = True


def make_form_readonly(form):
    for field in form.fields.values():
        make_field_readonly(field)


def initialize_form(FormClass, request, readonly=False, **kwargs):
    if not readonly and request.method == 'POST':
        form = FormClass(request.POST, **kwargs)
    else:
        form = FormClass(**kwargs)

    if readonly:
        make_form_readonly(form)

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
    # Checkboxen handled by pypugjs
    if isinstance(input, str):
        return input
    # Submits we need to handle ourselves
    else:
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
