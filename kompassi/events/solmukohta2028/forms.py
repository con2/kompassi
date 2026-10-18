from crispy_forms.layout import Fieldset, Layout
from django import forms

from kompassi.core.forms import horizontal_form_helper
from kompassi.labour.forms import AlternativeFormMixin
from kompassi.labour.models import JobCategory, Signup

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Additional information",
                "email_alias",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = ("email_alias",)


class OrganizerSignupForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        admin = kwargs.pop("admin")

        if admin:
            raise AssertionError("must not be admin")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Your role",
                "job_title",
            ),
        )

        self.fields["job_title"].label = "Job title"
        self.fields["job_title"].help_text = "What are you doing in the Solmukohta 2028 team?"
        self.fields["job_title"].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

        widgets = dict(  # noqa: RUF012
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="solmukohta2028", slug="organizers"))


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Email alias",
                "email_alias",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = ("email_alias",)

    def get_excluded_field_defaults(self):
        return dict()

    def get_excluded_m2m_field_defaults(self):
        return dict()
