from crispy_forms.layout import Fieldset, Layout
from django import forms
from kompassi.core.forms import horizontal_form_helper
from kompassi.labour.forms import AlternativeFormMixin, SignupForm
from kompassi.labour.models import Signup
from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Lisätiedot",
                "special_diet",
                "prior_experience",
                "free_text",
            )
        )

    class Meta:
        model = SignupExtra
        fields = (
            "special_diet",
            "prior_experience",
            "free_text",
        )


class OrganizerSignupForm(forms.ModelForm, AlternativeFormMixin):
    class Meta:
        model = Signup
        fields = ("job_title",)


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    class Meta:
        model = SignupExtra
        fields = ("special_diet",)

    def get_excluded_field_defaults(self):
        return dict(
            prior_experience="",
            free_text="Ilmoittautunut vastaavana",
        )
