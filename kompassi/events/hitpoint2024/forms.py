from datetime import timedelta

from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import horizontal_form_helper
from kompassi.labour.forms import AlternativeFormMixin
from kompassi.labour.models import JobCategory, Signup
from kompassi.zombies.programme.models import AlternativeProgrammeFormMixin, Category, Programme

from .models import SignupExtra

# TODO hitpoint2024: shirt_Size


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "shift_type",
            "total_work",
            "night_work",
            "construction",
            Fieldset(
                "Työtodistus",
                "want_certificate",
                "certificate_delivery_address",
            ),
            Fieldset(
                "Lisätiedot",
                "shirt_size",
                "special_diet",
                "special_diet_other",
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
            "night_work",
            "construction",
            "want_certificate",
            "certificate_delivery_address",
            "shirt_size",
            "special_diet",
            "special_diet_other",
            "prior_experience",
            "shift_wishes",
            "free_text",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
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
        return dict(job_categories=JobCategory.objects.filter(event__slug="hitpoint2024", name="Conitea"))


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
            shift_type="kaikkikay",
            total_work="yli12h",
            night_work="miel",
            construction=False,
            want_certificate=False,
            certificate_delivery_address="",
            prior_experience="",
            free_text="Syötetty käyttäen coniitin ilmoittautumislomaketta",
        )

    def get_excluded_m2m_field_defaults(self):
        return dict()


class ProgrammeOfferForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        if "admin" in kwargs:
            admin = kwargs.pop("admin")
        else:
            admin = False

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        for field_name in [
            "title",
        ]:
            self.fields[field_name].required = True

        if not admin:
            for field_name in [
                "description",
                # "video_permission",
                # "stream_permission",
                "photography",
                "rerun",
                # "encumbered_content",
            ]:
                self.fields[field_name].required = True

        self.fields["category"].queryset = Category.objects.filter(event=event, public=True)
        self.fields["category"].label = _("Topic")

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "category",
            "computer",
            "use_audio",
            "use_video",
            # "number_of_microphones",
            "tech_requirements",
            # "video_permission",
            # "stream_permission",
            # "encumbered_content",
            "photography",
            "rerun",
            "room_requirements",
            "requested_time_slot",
            "notes_from_host",
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


DESCRIPTION_HELP_TEXT = _(
    "Advertise your game to potential players. Also explain, what is expected of players "
    "and what kind of themes are involved. Be extra sure to inform about potentially "
    "shocking themes. Recommended length is 300–500 characters. We reserve the right "
    "to edit this as necessary (including but not limited to shortening)."
)
MAX_RUNS_HELP_TEXT = _(
    "How many times are you prepared to run this game? For free entry, you are expected to run a game for at least four hours."
)


class RpgForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("admin", False)
        kwargs.pop("event")

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "rpg_system",
            "approximate_length",
            "max_runs",
            "min_players",
            "max_players",
            "description",
            "three_word_description",
            "hitpoint2020_preferred_time_slots",
            "notes_from_host",
            Fieldset(
                _("Whom is the game for?"),
                "is_english_ok",
                "is_children_friendly",
                "is_age_restricted",
                "is_beginner_friendly",
            ),
        )

        self.fields["max_runs"].help_text = MAX_RUNS_HELP_TEXT

        self.fields["three_word_description"].required = True
        self.fields["three_word_description"].label = _("Summary in one sentence")
        self.fields["three_word_description"].help_text = _("Summarize the description of your game in one sentence.")

        self.fields["rpg_system"].required = True

        self.fields["description"].help_text = DESCRIPTION_HELP_TEXT
        self.fields["description"].required = True

        self.fields["is_english_ok"].label = _("In English")
        self.fields["is_english_ok"].help_text = _("Check this box if your RPG is played in English.")

    class Meta:
        model = Programme
        fields = (
            "title",
            "rpg_system",
            "approximate_length",
            "max_runs",
            "min_players",
            "max_players",
            "three_word_description",
            "description",
            "hitpoint2020_preferred_time_slots",
            "notes_from_host",
            "is_english_ok",
            "is_children_friendly",
            "is_age_restricted",
            "is_beginner_friendly",
        )

        widgets = dict(
            hitpoint2020_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="hitpoint2024", slug="roolipeli"),
        )


class FreeformForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    """
    If it is freeform
    But it is written on a form
    Then is it truly free of form?
    A questionable form of freedom
    """

    def __init__(self, *args, **kwargs):
        kwargs.pop("admin", False)
        kwargs.pop("event")

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "approximate_length",
            "max_runs",
            "min_players",
            "max_players",
            "description",
            "three_word_description",
            "room_requirements",
            "physical_play",
            "other_author",
            "hitpoint2020_preferred_time_slots",
            "notes_from_host",
            Fieldset(
                _("Whom is the game for?"),
                "is_english_ok",
                "is_children_friendly",
                "is_age_restricted",
                "is_beginner_friendly",
            ),
        )

        self.fields["max_runs"].help_text = MAX_RUNS_HELP_TEXT

        self.fields["three_word_description"].required = True
        self.fields["three_word_description"].label = _("Summary in one sentence")
        self.fields["three_word_description"].help_text = _("Summarize the description of your game in one sentence.")

        self.fields["description"].required = True
        self.fields["description"].help_text = DESCRIPTION_HELP_TEXT

        self.fields["is_english_ok"].label = _("In English")
        self.fields["is_english_ok"].help_text = _("Check this box if your RPG is played in English.")

    class Meta:
        model = Programme
        fields = (
            "title",
            "approximate_length",
            "max_runs",
            "min_players",
            "max_players",
            "description",
            "three_word_description",
            "room_requirements",
            "physical_play",
            "other_author",
            "hitpoint2020_preferred_time_slots",
            "notes_from_host",
            "is_english_ok",
            "is_children_friendly",
            "is_age_restricted",
            "is_beginner_friendly",
        )

        widgets = dict(
            hitpoint2020_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="hitpoint2024", slug="freeform"),
        )


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


class AfterpartyParticipationSurvey(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")

        super().__init__(*args, **kwargs)

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
            "special_diet",
            "special_diet_other",
        )
        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )
