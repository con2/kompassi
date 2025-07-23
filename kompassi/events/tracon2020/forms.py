from datetime import timedelta

from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.utils.translation import gettext_lazy as _
from zombies.hitpoint2017.forms import (
    APPROXIMATE_LENGTH_HELP_TEXT,
)
from zombies.hitpoint2017.forms import (
    DESCRIPTION_HELP_TEXT as RPG_DESCRIPTION_HELP_TEXT,
)

from kompassi.core.utils import horizontal_form_helper, indented_without_label
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
            "shift_type",
            "total_work",
            indented_without_label("overseer"),
            Fieldset(
                "Työtodistus",
                indented_without_label("want_certificate"),
                "certificate_delivery_address",
            ),
            Fieldset(
                "Lisätiedot",
                "shirt_size",
                "special_diet",
                "special_diet_other",
                "lodging_needs",
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
            "overseer",
            "want_certificate",
            "certificate_delivery_address",
            "shirt_size",
            "special_diet",
            "special_diet_other",
            "lodging_needs",
            "prior_experience",
            "shift_wishes",
            "free_text",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            lodging_needs=forms.CheckboxSelectMultiple,
        )

    def clean_certificate_delivery_address(self):
        want_certificate = self.cleaned_data["want_certificate"]
        certificate_delivery_address = self.cleaned_data["certificate_delivery_address"]

        if want_certificate and not certificate_delivery_address:
            raise forms.ValidationError(
                "Koska olet valinnut haluavasi työtodistuksen, on työtodistuksen toimitusosoite täytettävä."
            )

        return certificate_delivery_address


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

        self.fields["job_title"].help_text = "Mikä on tehtäväsi coniteassa? Printataan badgeen."
        # self.fields['job_title'].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="tracon2020", name="Conitea"))

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
                "shirt_size",
                "special_diet",
                "special_diet_other",
                "email_alias",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            "shirt_size",
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
            overseer=False,
            want_certificate=False,
            certificate_delivery_address="",
            prior_experience="",
            free_text="Syötetty käyttäen coniitin ilmoittautumislomaketta",
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            lodging_needs=[],
        )


class ProgrammeSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "shirt_size",
            "special_diet",
            "special_diet_other",
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

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "long_description",
            "length_from_host",
            "category",
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
            "requested_time_slot",
            "notes_from_host",
        )


class RpgForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        admin = kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "rpg_system",
            "approximate_length",
            "min_players",
            "max_players",
            "description",
            "three_word_description",
            "hitpoint2017_preferred_time_slots",
            "notes_from_host",
            Fieldset(
                _("Whom is the game for?"),
                "is_english_ok",
                "is_children_friendly",
                "is_age_restricted",
                "is_beginner_friendly",
                "is_intended_for_experienced_participants",
            ),
        )

        self.fields["approximate_length"].help_text = APPROXIMATE_LENGTH_HELP_TEXT

        if not admin:
            for field_name in [
                "three_word_description",
                "rpg_system",
                "description",
            ]:
                self.fields[field_name].required = True

        self.fields["description"].help_text = RPG_DESCRIPTION_HELP_TEXT

    class Meta:
        model = Programme
        fields = (
            "title",
            "rpg_system",
            "approximate_length",
            "min_players",
            "max_players",
            "three_word_description",
            "description",
            "hitpoint2017_preferred_time_slots",
            "notes_from_host",
            "is_english_ok",
            "is_children_friendly",
            "is_age_restricted",
            "is_beginner_friendly",
            "is_intended_for_experienced_participants",
        )

        widgets = dict(
            hitpoint2017_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="tracon2020", slug="roolipeliohjelma"),
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


class SwagSurvey(forms.ModelForm):
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
        fields = ("shirt_size",)


class LodgingNeedsSurvey(forms.ModelForm):
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
        fields = ("lodging_needs",)
        widgets = dict(
            lodging_needs=forms.CheckboxSelectMultiple,
        )


class AfterpartyParticipationSurvey(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.fields["afterparty_participation"].label = "Osallistun iltabileisiin"
        self.fields[
            "afterparty_participation"
        ].help_text = "Ruksaa tämä ruutu, mikäli haluat osallistua kaatajaisiin. Mikäli mielesi muuttuu tai sinulle tulee este, peru ilmoittautumisesi poistamalla rasti tästä ruudusta."

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    @classmethod
    def get_instance_for_event_and_person(cls, event, person):
        year = event.start_time.year
        t = event.start_time.date().replace(year=year - 18) + timedelta(days=15)
        return SignupExtra.objects.get(
            event=event,
            person=person,
            person__birth_date__lte=t,
            is_active=True,
        )

    class Meta:
        model = SignupExtra
        fields = (
            "afterparty_participation",
            # 'pick_your_poison',
            "special_diet",
            "special_diet_other",
            # 'afterparty_help',
        )
        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            # pick_your_poison=forms.CheckboxSelectMultiple,
        )
