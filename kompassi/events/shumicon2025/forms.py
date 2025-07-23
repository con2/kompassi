from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import horizontal_form_helper
from kompassi.labour.forms import AlternativeFormMixin
from kompassi.labour.models import JobCategory, Signup
from kompassi.zombies.programme.models import AlternativeProgrammeFormMixin, Category, Programme

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "shift_leader",
            "shift_type",
            "build_participation",
            Fieldset(
                _("Language skills"),
                "native_language",
                "native_language_other",
                "known_language",
                "known_language_other",
            ),
            Fieldset(
                "Lisätiedot",
                "special_diet",
                "special_diet_other",
                "shift_wishes",
                "why_work",
                "why_you",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shift_type",
            "shift_leader",
            "shirt_size",
            "build_participation",
            "native_language",
            "native_language_other",
            "known_language",
            "known_language_other",
            "special_diet",
            "special_diet_other",
            "shift_wishes",
            "why_work",
            "why_you",
        )

        widgets = dict(
            native_language=forms.CheckboxSelectMultiple,
            native_language_other=forms.TextInput,
            known_language=forms.CheckboxSelectMultiple,
            special_diet=forms.CheckboxSelectMultiple,
            work_days=forms.CheckboxSelectMultiple,
        )


class OrganizerSignupForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        admin = kwargs.pop("admin")

        if admin:
            raise NotImplementedError("admin=True")

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
        return dict(
            job_categories=JobCategory.objects.filter(event__slug="shumicon2025", name="Vastaava"),
            # work_days=EventDay.objects.all(),
        )


class ProgrammeSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "special_diet",
            "special_diet_other",
        )

    class Meta:
        model = SignupExtra
        fields = (
            "special_diet",
            "special_diet_other",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            # work_days=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            shift_type="none",
            total_work="8h",
            free_text="Syötetty käyttäen ohjelmanjärjestäjän ilmoittautumislomaketta",
        )


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Lisätiedot",
                "build_participation",
                "shirt_size",
                "special_diet",
                "special_diet_other",
                "parking_needed",
                "car_regnr",
                Fieldset(
                    _("Language skills"),
                    "native_language",
                    "native_language_other",
                    "known_language",
                    "known_language_other",
                ),
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shirt_size",
            "build_participation",
            "parking_needed",
            "car_regnr",
            "native_language",
            "native_language_other",
            "known_language",
            "known_language_other",
            "special_diet",
            "special_diet_other",
        )

        widgets = dict(
            car_regnr=forms.TextInput,
            native_language=forms.CheckboxSelectMultiple,
            native_language_other=forms.TextInput,
            known_language=forms.CheckboxSelectMultiple,
            special_diet=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            shift_type="kaikkikay",
            total_work="yli12h",
            construction=False,
            # overseer=False,
            # need_lodging=False,
            # want_certificate=True,
            # certificate_delivery_address="",
            prior_experience="",
            free_text="Syötetty käyttäen coniitin ilmoittautumislomaketta",
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            # work_days=EventDay.objects.all(),
        )


class ProgrammeForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        admin = kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset(
                _("Programme content"),
                "title",
                "description",
                "long_description",
                "category",
                "requested_time_slot",
            ),
            Fieldset(
                _("Technical details"),
                "computer",
                "use_audio",
                "use_video",
                "number_of_microphones",
                "tech_requirements",
            ),
            Fieldset(
                _("Other details"),
                "stream_permission",
                "encumbered_content",
                "photography",
                "rerun",
                "rerun_extra",
                "room_requirements",
                "notes_from_host",
            ),
        )

        self.fields["title"].required = True
        if not admin:
            for field_name in [
                "description",
                "encumbered_content",
                "photography",
                "rerun",
                "stream_permission",
            ]:
                self.fields[field_name].required = True

        self.fields["category"].queryset = Category.objects.filter(event=event, public=True)  # type: ignore

        self.fields["description"].help_text = (
            "Tämä kuvaus julkaistaan web-ohjelmakartassa sekä mahdollisessa ohjelmalehdessä. Kuvauksen "
            "tarkoitus on antaa osallistujalle riittävät tiedot päättää, osallistuako ohjelmaasi, sekä "
            "markkinoida ohjelmaasi. Pidä kuvaus kuitenkin ytimekkäänä, jotta se mahtuisi ohjelmalehteen. "
            "Ohjelmakuvauksen maksimipituus ohjelmalehteä varten on 400 merkkiä. Varaamme oikeuden muokata kuvausta."
        )
        self.fields["description"].max_length = 400

        self.fields[
            "room_requirements"
        ].help_text = "Miten suurta yleisöä odotat ohjelmallesi? Minkä tyyppistä tilaa toivot ohjelmallesi? Minkälaisia kalusteita tarvitset ohjelmaasi varten? (Luentosaleissa löytyy paikat puhujille ja penkit yleisölle, näitä ei tarvitse tässä listata.)"

        self.fields["stream_permission"].choices = [  # type: ignore
            (k, t) for (k, t) in self.fields["stream_permission"].choices if k != "please"
        ]

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "long_description",
            "tracon2023_accessibility_warnings",
            "tracon2023_content_warnings",
            "category",
            "requested_time_slot",
            "computer",
            "use_audio",
            "use_video",
            "number_of_microphones",
            "tech_requirements",
            "stream_permission",
            "encumbered_content",
            "photography",
            "rerun",
            "rerun_extra",
            "room_requirements",
            "notes_from_host",
        )

        widgets = dict(
            tracon2023_accessibility_warnings=forms.CheckboxSelectMultiple,
            tracon2023_preferred_time_slots=forms.CheckboxSelectMultiple,
        )
