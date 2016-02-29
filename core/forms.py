# encoding: utf-8

from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden

from core.utils import DateField, indented_without_label

from .models import Person, EMAIL_LENGTH, PHONE_NUMBER_LENGTH, BIRTH_DATE_HELP_TEXT
from .utils import horizontal_form_helper, check_password_strength


valid_username = RegexValidator(
    regex=r'^[a-z0-9_]{4,30}$',
    message=_(u'Invalid user name'),
)


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=30, label=_(u'User name or e-mail address'))

    password = forms.CharField(
        required=True,
        max_length=1023,
        label=_(u'Password'),
        widget=forms.PasswordInput,
    )

    next = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'next',
            'username',
            'password',
        )


class PersonForm(forms.ModelForm):
    birth_date = DateField(required=True, label=_(u'Birth date'), help_text=BIRTH_DATE_HELP_TEXT)

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)

        for field_name in [
            'email',
            'phone'
        ]:
            self.fields[field_name].required = True

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        layout_parts = [
            Fieldset(_(u'Basic information'),
                'first_name',
                'surname',
                'nick',
                'preferred_name_display_style',
                'birth_date',
            ),
            Fieldset(_(u'Membership roster information'),
                'official_first_names',
                'muncipality',
            ),
            Fieldset(_(u'Contact information'),
                'phone',
                'email',
            ),
            Fieldset(_(u'Privacy'),
                'may_send_info',
                'allow_work_history_sharing',
            )
        ]

        self.helper.layout = Layout(*layout_parts)

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = Person.objects.filter(email=email, user__isnull=False)

        if qs.exists() and self.instance not in qs:
            raise forms.ValidationError(_(
                u'There is already a user account associated with this e-mail address. '
                u'If you have forgotten your password, please do not create another user '
                u'account but rather restore your password using the Forgot password link '
                u'at the sign in form.'
            ))

        return email

    def clean_first_name(self):
        # ipa will barf on leading/trailing whitespace
        first_name = self.cleaned_data['first_name']

        if first_name:
            first_name = first_name.strip()

        return first_name

    def clean_surname(self):
        # ipa will barf on leading/trailing whitespace
        surname = self.cleaned_data['surname']

        if surname:
            surname = surname.strip()

        return surname

    class Meta:
        model = Person
        fields = (
            'allow_work_history_sharing',
            'birth_date',
            'email',
            'first_name',
            'may_send_info',
            'muncipality',
            'nick',
            'phone',
            'official_first_names',
            'preferred_name_display_style',
            'surname',
        )


PASSWORD_HELP_TEXT = _(
    u'The password must consist of at least %(min_length)d characters and contain '
    u'%(min_classes)d of the following: small letter, capital letter, number, special character.'
) % dict(
    min_classes=settings.KOMPASSI_PASSWORD_MIN_CLASSES,
    min_length=settings.KOMPASSI_PASSWORD_MIN_LENGTH,
)


class RegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=30,
        validators=[valid_username],
        label=_(u'User name'),
        help_text=_(
            u'Please choose a user name. The user name must consist of 4 to 30 characters. '
            u'The following characters are allowed: <b>small</b> letters <i>a&ndash;z</i>, numbers <i>0&ndash;9</i> '
            u'and underscore </i>_</i>. You can use either this user name or your e-mail address to sign in.'
        )
    )

    password = forms.CharField(
        required=True,
        max_length=1023,
        label=_(u'Password'),
        widget=forms.PasswordInput,
        validators=[check_password_strength],
    )
    password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=_(u'Password (again)'),
        widget=forms.PasswordInput,
        help_text=PASSWORD_HELP_TEXT,
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(_(u'User name and password'),
                'username',
                'password',
                'password_again'
            ),
        )

    def clean_username(self):
        from django.contrib.auth.models import User

        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_(u'This user name is already taken.'))

        return username

    def clean_password_again(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')

        if password and password_again and password != password_again:
            raise forms.ValidationError(_(u'Passwords do not match.'))

        return password_again


class TermsAndConditionsForm(forms.Form):
    accept_terms_and_conditions = forms.BooleanField(
        required=True,
        label=_(
            u'I hereby authorize the use of my personal information as outlined in the privacy policy. '
            u'See site footer for a link to the privacy policy. <em>(mandatory)</em>'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(TermsAndConditionsForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False


class PasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        max_length=1023,
        label=_(u'Old password'),
        widget=forms.PasswordInput,
    )

    new_password = forms.CharField(
        required=True,
        max_length=1023,
        label=_(u'New password'),
        widget=forms.PasswordInput,
        validators=[check_password_strength],
    )

    new_password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=_(u'New password (again)'),
        widget=forms.PasswordInput,
        help_text=PASSWORD_HELP_TEXT,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('the_request')

        super(PasswordForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            Fieldset(_(u'Change password'),
                'old_password',
                'new_password',
                'new_password_again',
            ),
            indented_without_label(Submit('submit', _(u'Change password'), css_class='btn-primary'))
        )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        authenticated_user = authenticate(
            username=self.request.user.username,
            password=old_password
        )

        if not authenticated_user:
            raise forms.ValidationError(_(u'Wrong password.'))

        return old_password

    def clean_new_password_again(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_again = self.cleaned_data.get('new_password_again')

        if new_password and new_password_again and new_password != new_password_again:
            raise forms.ValidationError(_(u'The passwords do not match.'))

        return new_password_again


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True, max_length=EMAIL_LENGTH, label=_(u'E-mail address'))

    def __init__(self, *args, **kwargs):
        super(PasswordResetRequestForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            'email',
            indented_without_label(Submit('submit', _(u'Submit'), css_class='btn-success'))
        )

class PasswordResetForm(forms.Form):
    # XXX BEGIN UGLY COPYPASTA
    new_password = forms.CharField(
        required=True,
        max_length=1023,
        label=_(u'New password'),
        widget=forms.PasswordInput,
        validators=[check_password_strength],
    )

    new_password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=_(u'New password (again)'),
        widget=forms.PasswordInput,
        help_text=PASSWORD_HELP_TEXT,
    )

    def clean_new_password_again(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_again = self.cleaned_data.get('new_password_again')

        if new_password and new_password_again and new_password != new_password_again:
            raise forms.ValidationError(_(u'The passwords do not match.'))

        return new_password_again
    # XXX END UGLY COPYPASTA

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            'new_password',
            'new_password_again',
            indented_without_label(Submit('submit', _(u'Change password'), css_class='btn-success'))
        )
