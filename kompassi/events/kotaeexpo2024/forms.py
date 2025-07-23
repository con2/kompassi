from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import horizontal_form_helper, indented_without_label
from kompassi.labour.forms import AlternativeFormMixin, SignupForm
from kompassi.labour.models import JobCategory, Signup
from kompassi.zombies.programme.models import AlternativeProgrammeFormMixin, Category, Programme

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
        return dict(job_categories=JobCategory.objects.filter(event__slug="kotaeexpo2024", name="Vastaava"))

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
                "email_alias",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "special_diet",
            "special_diet_other",
            "email_alias",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
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

        return Q(event__slug="kotaeexpo2024", public=False) & ~Q(slug="vastaava")

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


class ProgrammeSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = SignupExtra
        fields = ()

    def get_excluded_field_defaults(self):
        return dict(
            free_text="Syötetty käyttäen ohjelmanjärjestäjän ilmoittautumislomaketta",
            shift_type="kaikkikay",
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
                "length_from_host",
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

        self.fields["category"].queryset = Category.objects.filter(event=event, public=True)

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

        self.fields["stream_permission"].choices = [
            (k, t) for (k, t) in self.fields["stream_permission"].choices if k != "please"
        ]

        self.fields["length_from_host"].label = "Ohjelman pituus"
        self.fields["length_from_host"].help_text = "Kuinka kauan ohjelmasi kestää?"

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "long_description",
            "category",
            "length_from_host",
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
