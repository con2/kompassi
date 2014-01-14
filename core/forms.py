# encoding: utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden

from core.utils import DateField

from .models import Person, EMAIL_LENGTH, PHONE_NUMBER_LENGTH, BIRTH_DATE_HELP_TEXT
from .utils import horizontal_form_helper, indented_without_label


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
    birth_date = DateField(required=True, label=u'Syntymäaika', help_text=BIRTH_DATE_HELP_TEXT)
    email = forms.EmailField(required=True, max_length=EMAIL_LENGTH, label=u'Sähköpostiosoite')
    phone = forms.CharField(required=True, max_length=PHONE_NUMBER_LENGTH, label=u'Puhelinnumero')

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            Fieldset(u'Perustiedot',
                'first_name',
                'surname',
                'nick',
                'birth_date'
            ),
            Fieldset(u'Yhteystiedot',
                'email',
                'phone'
            ),
            indented_without_label(Submit('submit', u'Tallenna', css_class='btn-primary'))

        )

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
