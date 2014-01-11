from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden


def initialize_form(FormClass, request, *args, **kwargs):
    if request.method == 'POST':
        return FormClass(request.POST, *args, **kwargs)
    else:
        return FormClass(*args, **kwargs)


def indented_without_label(input):
    return Div(Div(input, css_class='controls col-md-2 col-md-offset-2'), css_class='form-group')


def horizontal_form_helper():
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-2'
    helper.field_class = 'col-md-4'
    return helper