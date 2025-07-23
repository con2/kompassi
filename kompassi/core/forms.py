from crispy_forms.layout import Fieldset, Layout, Submit
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import DateField, indented_without_label

from .models import BIRTH_DATE_HELP_TEXT, EMAIL_LENGTH, Person
from .utils import horizontal_form_helper, validate_password

valid_username = RegexValidator(
    regex=r"^[a-z0-9_]{4,30}$",
    message="Invalid user name",
)

PASSWORD_HELP_TEXT = _("Please use a strong password.")


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=EMAIL_LENGTH, label=_("User name or e-mail address"))

    password = forms.CharField(
        required=True,
        max_length=1023,
        label=_("Password"),
        widget=forms.PasswordInput,
    )

    next = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.label_class = "col-md-4"
        self.helper.field_class = "col-md-8"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "next",
            "username",
            "password",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]

        if username:
            username = username.lower().strip()

        return username


class PersonFormMixin:
    def clean_email(self):
        email = self.cleaned_data["email"]

        if email:
            email = email.lower().strip()
            qs = Person.objects.filter(email__iexact=email, user__isnull=False)

            if qs.exists() and self.instance not in qs:
                raise forms.ValidationError(
                    _(
                        "There is already a user account associated with this e-mail address. "
                        "If you have forgotten your password, please do not create another user "
                        "account but rather restore your password using the Forgot password link "
                        "at the sign in form."
                    )
                )

        return email

    def clean_first_name(self):
        # ipa will barf on leading/trailing whitespace
        first_name = self.cleaned_data["first_name"]

        if first_name:
            first_name = first_name.strip()

        return first_name

    def clean_surname(self):
        # ipa will barf on leading/trailing whitespace
        surname = self.cleaned_data["surname"]

        if surname:
            surname = surname.strip()

        return surname


class PersonForm(PersonFormMixin, forms.ModelForm):
    birth_date = DateField(required=True, label=_("Birth date"), help_text=BIRTH_DATE_HELP_TEXT)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ["email", "phone"]:
            self.fields[field_name].required = True

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset(
                _("Basic information"),
                "first_name",
                "surname",
                "nick",
                "birth_date",
            ),
            Fieldset(
                _("Membership roster information"),
                "official_first_names",
                "muncipality",
            ),
            Fieldset(
                _("Contact information"),
                "phone",
                "email",
                "discord_handle",
            ),
            Fieldset(
                _("Privacy"),
                "preferred_badge_name_display_style",
                "preferred_name_display_style",
                "may_send_info",
                "allow_work_history_sharing",
            ),
        )

    class Meta:
        model = Person
        fields = (
            "first_name",
            "surname",
            "nick",
            "birth_date",
            "official_first_names",
            "muncipality",
            "phone",
            "email",
            "discord_handle",
            "preferred_badge_name_display_style",
            "preferred_name_display_style",
            "may_send_info",
            "allow_work_history_sharing",
        )


class RegistrationPersonForm(PersonFormMixin, forms.ModelForm):
    birth_date = DateField(required=True, label=_("Birth date"), help_text=BIRTH_DATE_HELP_TEXT)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ["email", "phone"]:
            self.fields[field_name].required = True

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset(
                _("Basic information"),
                "first_name",
                "surname",
                "nick",
                "birth_date",
            ),
            Fieldset(
                _("Contact information"),
                "phone",
                "email",
            ),
            Fieldset(
                _("Privacy"),
                "may_send_info",
            ),
        )

    class Meta:
        model = Person
        fields = (
            "first_name",
            "surname",
            "nick",
            "birth_date",
            "phone",
            "email",
            "may_send_info",
        )


class RegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=30,
        validators=[valid_username],
        label=_("User name"),
        help_text=_(
            "Please choose a user name. The user name must consist of 4 to 30 characters. "
            "The following characters are allowed: <b>small</b> letters <i>a&ndash;z</i>, numbers <i>0&ndash;9</i> "
            "and underscore </i>_</i>. You can use either this user name or your e-mail address to sign in."
        ),
    )

    password = forms.CharField(
        required=True,
        max_length=1023,
        label=_("Password"),
        widget=forms.PasswordInput,
        validators=[validate_password],
    )
    password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=_("Password (again)"),
        widget=forms.PasswordInput,
        help_text=PASSWORD_HELP_TEXT,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(_("User name and password"), "username", "password", "password_again"),
        )

    def clean_username(self):
        from django.contrib.auth.models import User

        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("This user name is already taken."))

        return username

    def clean_password_again(self):
        password = self.cleaned_data.get("password")
        password_again = self.cleaned_data.get("password_again")

        if password and password_again and password != password_again:
            raise forms.ValidationError(_("Passwords do not match."))

        return password_again


class TermsAndConditionsForm(forms.Form):
    accept_terms_and_conditions = forms.BooleanField(
        required=True,
        label=_(
            "I hereby authorize the use of my personal information as outlined in the privacy policy. "
            "See site footer for a link to the privacy policy. <em>(mandatory)</em>"
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False


class PasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        max_length=1023,
        label=_("Old password"),
        widget=forms.PasswordInput,
    )

    new_password = forms.CharField(
        required=True,
        max_length=1023,
        label=_("New password"),
        widget=forms.PasswordInput,
        validators=[validate_password],
    )

    new_password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=_("New password (again)"),
        widget=forms.PasswordInput,
        help_text=PASSWORD_HELP_TEXT,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("the_request")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            Fieldset(
                _("Change password"),
                "old_password",
                "new_password",
                "new_password_again",
            ),
            indented_without_label(Submit("submit", _("Change password"), css_class="btn-primary")),
        )

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")

        authenticated_user = authenticate(username=self.request.user.username, password=old_password)

        if not authenticated_user:
            raise forms.ValidationError(_("Wrong password."))

        return old_password

    def clean_new_password_again(self):
        new_password = self.cleaned_data.get("new_password")
        new_password_again = self.cleaned_data.get("new_password_again")

        if new_password and new_password_again and new_password != new_password_again:
            raise forms.ValidationError(_("The passwords do not match."))

        return new_password_again


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True, max_length=EMAIL_LENGTH, label=_("E-mail address"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            "email", indented_without_label(Submit("submit", _("Submit"), css_class="btn-success"))
        )

    def clean_email(self):
        email = self.cleaned_data["email"]

        if email:
            email = email.lower().strip()

        return email


class PasswordResetForm(forms.Form):
    # XXX BEGIN UGLY COPYPASTA
    new_password = forms.CharField(
        required=True,
        max_length=1023,
        label=_("New password"),
        widget=forms.PasswordInput,
        validators=[validate_password],
    )

    new_password_again = forms.CharField(
        required=True,
        max_length=1023,
        label=_("New password (again)"),
        widget=forms.PasswordInput,
        help_text=PASSWORD_HELP_TEXT,
    )

    def clean_new_password_again(self):
        new_password = self.cleaned_data.get("new_password")
        new_password_again = self.cleaned_data.get("new_password_again")

        if new_password and new_password_again and new_password != new_password_again:
            raise forms.ValidationError(_("The passwords do not match."))

        return new_password_again

    # XXX END UGLY COPYPASTA

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            "new_password",
            "new_password_again",
            indented_without_label(Submit("submit", _("Change password"), css_class="btn-success")),
        )
