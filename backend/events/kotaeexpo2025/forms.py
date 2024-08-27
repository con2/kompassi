from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.db.models import Q

from core.utils import horizontal_form_helper, indented_without_label
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
            "total_work",
            indented_without_label("night_shift"),
            indented_without_label("overseer"),
            Fieldset(
                "Työtodistus",
                indented_without_label("want_certificate"),
            ),
            Fieldset(
                "Millä kielellä olet valmis palvelemaan asiakkaita?",
                "known_language",
                "known_language_other",
            ),
            Fieldset(
                "Lisätiedot",
                "special_diet",
                "special_diet_other",
                "accommodation",
                "prior_experience",
                "shift_wishes",
                "free_text",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shift_type",
            "total_work",
            "night_shift",
            "overseer",
            "want_certificate",
            "known_language",
            "known_language_other",
            "special_diet",
            "special_diet_other",
            "accommodation",
            "prior_experience",
            "shift_wishes",
            "free_text",
        )

        widgets = dict(
            known_language=forms.CheckboxSelectMultiple,
            special_diet=forms.CheckboxSelectMultiple,
            accommodation=forms.CheckboxSelectMultiple,
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

        self.fields["job_title"].help_text = "Mikä on vastuualueesi? Printataan badgeen."
        self.fields["job_title"].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="kotaeexpo2025", name="Vastaava"))

    def get_excluded_field_defaults(self):
        return dict(
            total_work="yli10h",
        )


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
                "accommodation",
                "email_alias",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "special_diet",
            "special_diet_other",
            "accommodation",
            "email_alias",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            accommodation=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            shift_type="kaikkikay",
            total_work="yli10h",
            night_shift=False,
            overseer=False,
            want_certificate=False,
            prior_experience="",
            free_text="Syötetty käyttäen coniitin ilmoittautumislomaketta",
        )


class SpecialistSignupForm(SignupForm, AlternativeFormMixin):
    def get_job_categories_query(self, event, admin=False):
        if admin:
            raise AssertionError("must not be admin")

        return Q(event__slug="kotaeexpo2025", public=False) & ~Q(slug="vastaava")

    def get_excluded_field_defaults(self):
        return dict(
            notes="Syötetty käyttäen erikoistehtävien ilmoittautumislomaketta",
        )


class SpecialistSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "shift_type",
            "total_work",
            indented_without_label("night_shift"),
            indented_without_label("overseer"),
            Fieldset(
                "Työtodistus",
                indented_without_label("want_certificate"),
            ),
            Fieldset(
                "Millä kielellä olet valmis palvelemaan asiakkaita?",
                "known_language",
                "known_language_other",
            ),
            Fieldset(
                "Lisätiedot",
                "special_diet",
                "special_diet_other",
                "accommodation",
                "prior_experience",
                "shift_wishes",
                "free_text",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shift_type",
            "total_work",
            "night_shift",
            "overseer",
            "want_certificate",
            "known_language",
            "known_language_other",
            "special_diet",
            "special_diet_other",
            "accommodation",
            "prior_experience",
            "shift_wishes",
            "free_text",
        )

        widgets = dict(
            known_language=forms.CheckboxSelectMultiple,
            special_diet=forms.CheckboxSelectMultiple,
            accommodation=forms.CheckboxSelectMultiple,
        )


class ShiftWishesSurvey(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    @classmethod
    def get_instance_for_event_and_person(cls, event, person):
        return SignupExtra.objects.get(event=event, person=person)

    class Meta:
        model = SignupExtra
        fields = ("shift_wishes",)
