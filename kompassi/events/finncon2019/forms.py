from crispy_forms.layout import Fieldset, Layout
from django import forms

from kompassi.core.utils import horizontal_form_helper
from kompassi.labour.forms import AlternativeFormMixin
from kompassi.labour.models import JobCategory, Signup
from kompassi.zombies.programme.forms.misc_forms import AlternativeProgrammeFormMixin
from kompassi.zombies.programme.models import Category, Programme

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
                "shirt_size",
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
            "shirt_size",
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
        admin = kwargs.pop("admin")

        assert not admin

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
        # self.fields['job_title'].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="finncon2019", name="Conitea"))


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


class ProgrammeForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        for field_name in [
            "title",
            "description",
            "length_from_host",
        ]:
            self.fields[field_name].required = True

        self.fields["category"].queryset = Category.objects.filter(event=event, public=True)

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "length_from_host",
            "language",
            "category",
            "computer",
            "use_audio",
            "use_video",
            "number_of_microphones",
            "tech_requirements",
            "video_permission",
            "encumbered_content",
            "photography",
            "rerun",
            "room_requirements",
            "requested_time_slot",
            "notes_from_host",
        )
