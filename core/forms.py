# encoding: utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden

from .models import Person, EMAIL_LENGTH, PHONE_NUMBER_LENGTH

def indented_without_label(input):
    return Div(Div(input, css_class='controls col-md-2 col-md-offset-2'), css_class='form-group')


def horizontal_form_helper():
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-2'
    helper.field_class = 'col-md-4'
    return helper


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            'username',
            'password',
            Hidden('next', '/'), # XXX
            indented_without_label(Submit('submit', u'Kirjaudu sisään', css_class='btn-primary'))
        )


class PersonForm(forms.ModelForm):
    birth_date = forms.DateField(required=True)
    email = forms.EmailField(required=True, max_length=EMAIL_LENGTH)
    phone = forms.CharField(required=True, max_length=PHONE_NUMBER_LENGTH)

    class Meta:
        model = Person
        fields = (
            'first_name',
            'surname',
            'nick',
            'birth_date',
            'email',
            'phone',
        )