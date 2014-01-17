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
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'username',
            'password',
        )


class PersonForm(forms.ModelForm):
    birth_date = DateField(required=True, label=u'Syntymäaika', help_text=BIRTH_DATE_HELP_TEXT)
    email = forms.EmailField(required=True, max_length=EMAIL_LENGTH, label=u'Sähköpostiosoite')
    phone = forms.CharField(required=True, max_length=PHONE_NUMBER_LENGTH, label=u'Puhelinnumero')

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()

        if self.instance.pk is None:
            save_button_text = u'Rekisteröidy'
        else:
            save_button_text = u'Tallenna tiedot'

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
            indented_without_label(Submit('submit', save_button_text, css_class='btn-primary'))
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


class RegistrationForm(forms.Form):
    username = forms.CharField(required=True, max_length=30, label=u'Käyttäjänimi')

    password = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Salasana',
        widget=forms.PasswordInput,
    )
    password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=u'Salasana uudestaan',
        widget=forms.PasswordInput,
    )

    accept_terms_and_conditions = forms.BooleanField(
        required=True,
        label=u'Annan luvan henkilötietojeni käsittelyyn rekisteriselosteen mukaisesti (TODO rekisteriseloste)'
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Käyttäjätunnus ja salasana',
                'username',
                'password',
                'password_again'
            ),
            Fieldset(u'Suostumus henkilötietojen käsittelyyn',
                indented_without_label('accept_terms_and_conditions')
            ),
        )

    def clean_username(self):
        from django.contrib.auth.models import User

        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'Käyttäjänimi on jo käytössä.')

        return username

    def clean_password_again(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')

        if password and password_again and password != password_again:
            raise forms.ValidationError(u'Salasanat eivät täsmää.')

        return password_again
