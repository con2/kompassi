from crispy_forms.layout import Fieldset, Layout
from django import forms

from kompassi.core.utils import horizontal_form_helper
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
            "total_work",
            Fieldset(
                "Lisätiedot",
                "dead_dog",
                "ika",
                "shirt_size",
                "color_wish",
                "special_diet",
                "special_diet_other",
                "prior_experience",
                "language_skills",
                "free_text",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "ika",
            "shirt_size",
            "color_wish",
            "dead_dog",
            "shift_type",
            "total_work",
            "special_diet",
            "special_diet_other",
            "prior_experience",
            "language_skills",
            "free_text",
        )
        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )


class OrganizerSignupForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin")
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Tehtävän tiedot",
                "job_title",
            ),
        )
        self.fields["job_title"].help_text = "Mikä on tehtäväsi coniteassa? Printataan badgeen."

    class Meta:
        model = Signup
        fields = ("job_title",)
        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="finncon2026", name="Conitea"))


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
            shift_type="yli4h",
            total_work="yli8h",
            prior_experience="",
            free_text="Syötetty käyttäen coniitin ilmoittautumislomaketta",
        )

    def get_excluded_m2m_field_defaults(self):
        return dict()
