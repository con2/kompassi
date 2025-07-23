from crispy_forms.layout import Fieldset, Layout
from django import forms

from kompassi.core.utils import horizontal_form_helper, indented_without_label
from kompassi.labour.forms import AlternativeFormMixin
from kompassi.labour.models import JobCategory, Signup

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "shift_type",
            indented_without_label("night_work"),
            Fieldset(
                "Lisätiedot",
                indented_without_label("need_lodging"),
                indented_without_label("want_certificate"),
                "shirt_size",
                "special_diet",
                "special_diet_other",
                "more_info",
                "prior_experience",
                "free_text",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shift_type",
            "shirt_size",
            "special_diet",
            "special_diet_other",
            "night_work",
            "need_lodging",
            "more_info",
            "want_certificate",
            "prior_experience",
            "free_text",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )


class OrganizerSignupForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        admin = kwargs.pop("admin")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Tehtävän tiedot",
                "job_title",
            ),
        )

        self.fields["job_title"].help_text = "Mikä on tehtäväsi vastaavana? Printataan badgeen."
        self.fields["job_title"].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

    def get_excluded_m2m_field_defaults(self):
        return dict(
            job_categories=JobCategory.objects.filter(event__slug="matsucon2023", name="Conitea"),
        )


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Lisätiedot",
                "shirt_size",
                "special_diet",
                "special_diet_other",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shirt_size",
            "special_diet",
            "special_diet_other",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            free_text="Syötetty käyttäen vastaavan ilmoittautumislomaketta",
            shift_type="lb",
        )

    def get_excluded_m2m_field_defaults(self):
        return dict()


ProgrammeSignupExtraForm = OrganizerSignupExtraForm
