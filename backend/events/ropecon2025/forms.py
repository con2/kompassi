from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.forms import horizontal_form_helper
from labour.forms import AlternativeFormMixin, SignupForm
from labour.models import JobCategory, Signup

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "shift_type",
            Fieldset(
                _("Work certificate"),
                "want_certificate",
            ),
            Fieldset(
                _("Language skills"),
                "languages",
                "other_languages",
            ),
            Fieldset(
                _("Additional information"),
                "special_diet",
                "special_diet_other",
                "prior_experience",
                "shift_wishes",
                "free_text",
            ),
            Fieldset(
                _("Consent for information processing"),
                "roster_publish_consent",
            ),
        )

        if "roster_publish_consent" in self.fields:
            self.fields["roster_publish_consent"].required = True

    class Meta:
        model = SignupExtra
        fields = (
            "shift_type",
            "want_certificate",
            "languages",
            "other_languages",
            "special_diet",
            "special_diet_other",
            "prior_experience",
            "shift_wishes",
            "free_text",
            "roster_publish_consent",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            languages=forms.CheckboxSelectMultiple,
        )


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
                "Tehtävän tiedot",
                "job_title",
            ),
        )

        self.fields["job_title"].help_text = "Mikä on tehtäväsi coniteassa? Printataan badgeen."
        self.fields["job_title"].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="ropecon2025", name="Conitea"))


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Lisätiedot",
                "special_diet",
                "special_diet_other",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "special_diet",
            "special_diet_other",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            shift_type="kaikkikay",
            want_certificate=False,
            prior_experience="",
            free_text="Syötetty käyttäen coniitin ilmoittautumislomaketta",
            roster_publish_consent=True,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict()


class SpecialistSignupForm(SignupForm, AlternativeFormMixin):
    def get_job_categories_query(self, event, admin=False):
        if admin:
            raise AssertionError("must not be admin")

        return Q(event__slug="ropecon2025", name__in=["Boffaus"])

    def get_excluded_field_defaults(self):
        return dict(
            notes="Syötetty käyttäen xxlomaketta",
        )


class SpecialistSignupExtraForm(SignupExtraForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "shift_type",
            Fieldset(
                _("Work certificate"),
                "want_certificate",
            ),
            Fieldset(
                _("Language skills"),
                "languages",
                "other_languages",
            ),
            Fieldset(
                _("Additional information"),
                "special_diet",
                "special_diet_other",
                "prior_experience",
                "shift_wishes",
                "free_text",
            ),
            Fieldset(
                _("Consent for information processing"),
                "roster_publish_consent",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shift_type",
            "want_certificate",
            "languages",
            "other_languages",
            "special_diet",
            "special_diet_other",
            "prior_experience",
            "shift_wishes",
            "free_text",
            "roster_publish_consent",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            languages=forms.CheckboxSelectMultiple,
        )
