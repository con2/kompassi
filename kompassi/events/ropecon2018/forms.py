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
            "shift_type",
            Fieldset(
                "Työtodistus",
                "want_certificate",
                "certificate_delivery_address",
            ),
            Fieldset(
                "Lisätiedot",
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
            "want_certificate",
            "certificate_delivery_address",
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
        self.fields["job_title"].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="ropecon2018", name="Conitea"))


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
            certificate_delivery_address="",
            prior_experience="",
            free_text="Syötetty käyttäen coniitin ilmoittautumislomaketta",
        )

    def get_excluded_m2m_field_defaults(self):
        return dict()


# XXX hack
ProgrammeSignupExtraForm = OrganizerSignupExtraForm


DESCRIPTION_HELP_TEXT = _(
    "Advertise your game to potential players. Also explain, what is expected of players "
    "and what kind of themes are involved. Be extra sure to inform about potentially "
    "shocking themes. Recommended length is 300–500 characters. We reserve the right "
    "to edit this as necessary (including but not limited to shortening)."
)

TALK_DESCRIPTION_HELP_TEXT = _(
    "Advertise your programme to potential participants. Be extra sure to inform about potentially "
    "shocking themes. Recommended length is 300–500 characters. We reserve the right "
    "to edit this as necessary (including but not limited to shortening)."
)

APPROXIMATE_LENGTH_HELP_TEXT = _(
    "In order to gain free entry, you are required to run at in total least four hours of games."
)

TALK_APPROXIMATE_LENGTH_HELP_TEXT = _("Talk programmes can be either 45 or 105 minutes in length.")

RPG_TITLE_HELP_TEXT = _("Game title.")

RPG_ENGLISH_NAME = _("Played in English")
RPG_ENGLISH_HELP_TEXT = _("Please tick this box if the game is hosted in English.")
RPG_EXPERIENCED_NAME = _("For experienced players")
RPG_EXPERIENCED_HELP_TEXT = _("Check this if the game requires knowledge of the world or the rules of the game.")
RPG_MIN_PLAYERS_HELP_TEXT = _(
    "Consider the minimum number of players carefully: you will maximize your chances of running the game by setting the number as low as possible."
)
RPG_NOTES_HELP_TEXT = _(
    "If there is anything else you wish to say to the RPG manager that is not covered by the above questions, please enter it here."
)

LARP_TITLE_HELP_TEXT = _("Think of a short title for your game. We reserve the right to alter the title.")
LARP_APPROXIMATE_LENGTH_HELP_TEXT = _(
    "You get one weekend ticket for one 4h game. The time includes setup, briefing, defriefing and game time."
)
LARP_DESCRIPTION_HELP_TEXT = _(
    "Advertise your game to potential players. Let the players know what is expected of them and what types of themes your game deals with. Please mention if your game deals with any difficult themes such as physical or mental violence. A good length for the description is 300-500 characters. We reserve the right to alter the description and the title if needed."
)
LARP_THREE_WORD_HELP_TEXT = _("Describe your game in three words, eg. genre, theme and mood.")
LARP_OTHER_AUTHOR_HELP_TEXT = _(
    "If the game has been written by somebody else than a GM running it in Ropecon, the writer must be mentioned here."
)
LARP_TIMESLOTS_HELP_TEXT = _(
    "When would you like to run your game? Time slots are intentionally vague. If you have detailed requests about the time slots, please let us know in the notes field."
)
LARP_NOTES_HELP_TEXT = _(
    "If you have any other comments to the larp team please write them here. Please mention if your game requires any of the characters to be of a certain gender/sex. Regardless of their gender/sex all characters should be playable by all players."
)
LARP_ENGLISH_OK_VERBOSE_NAME = _("Game can be run in English")
LARP_ENGLISH_OK_HELP_TEXT = _(
    "Check this box if you are capable, prepared and interested in running your game in English."
)
LARP_AGE_RESTRICTED_HELP_TEXT = _(
    "Check this box if your game includes themes that require the players to be at least 18 years of age."
)
LARP_BEGINNER_FRIENDLY_HELP_TEXT = _("Check this box if your game does not require prior larping experience.")


class RpgForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "rpg_system",
            Fieldset(
                _("Whom is the game for?"),
                "is_english_ok",
                "is_children_friendly",
                "is_age_restricted",
                "is_beginner_friendly",
                "is_intended_for_experienced_participants",
            ),
            Fieldset(
                _("Game genre (Choose all that apply)"),
                "ropecon2018_genre_fantasy",
                "ropecon2018_genre_scifi",
                "ropecon2018_genre_historical",
                "ropecon2018_genre_modern",
                "ropecon2018_genre_war",
                "ropecon2018_genre_horror",
                "ropecon2018_genre_exploration",
                "ropecon2018_genre_mystery",
                "ropecon2018_genre_drama",
                "ropecon2018_genre_humor",
            ),
            Fieldset(
                _("Game style (Choose any that apply)"),
                "ropecon2018_style_serious",
                "ropecon2018_style_light",
                "ropecon2018_style_rules_heavy",
                "ropecon2018_style_rules_light",
                "ropecon2018_style_story_driven",
                "ropecon2018_style_character_driven",
                "ropecon2018_style_combat_driven",
            ),
            Fieldset(
                _("Basic game information"),
                "approximate_length",
                "min_players",
                "max_players",
                "ropecon2018_preferred_time_slots",
                "description",
                "notes_from_host",
            ),
        )

        self.fields["title"].help_text = RPG_TITLE_HELP_TEXT

        self.fields["is_english_ok"].verbose_name = RPG_ENGLISH_NAME
        self.fields["is_english_ok"].help_text = RPG_ENGLISH_HELP_TEXT

        self.fields["is_intended_for_experienced_participants"].verbose_name = RPG_EXPERIENCED_NAME
        self.fields["is_intended_for_experienced_participants"].help_text = RPG_EXPERIENCED_HELP_TEXT

        self.fields["approximate_length"].initial = 240

        self.fields["rpg_system"].required = True

        self.fields["min_players"].help_text = RPG_MIN_PLAYERS_HELP_TEXT

        self.fields["description"].help_text = DESCRIPTION_HELP_TEXT
        self.fields["description"].required = True

        self.fields["notes_from_host"].help_text = RPG_NOTES_HELP_TEXT

    class Meta:
        model = Programme
        fields = (
            "title",
            "rpg_system",
            "is_english_ok",
            "is_children_friendly",
            "is_age_restricted",
            "is_beginner_friendly",
            "is_intended_for_experienced_participants",
            "ropecon2018_genre_fantasy",
            "ropecon2018_genre_scifi",
            "ropecon2018_genre_historical",
            "ropecon2018_genre_modern",
            "ropecon2018_genre_war",
            "ropecon2018_genre_horror",
            "ropecon2018_genre_exploration",
            "ropecon2018_genre_mystery",
            "ropecon2018_genre_drama",
            "ropecon2018_genre_humor",
            "ropecon2018_style_serious",
            "ropecon2018_style_light",
            "ropecon2018_style_rules_heavy",
            "ropecon2018_style_rules_light",
            "ropecon2018_style_story_driven",
            "ropecon2018_style_character_driven",
            "ropecon2018_style_combat_driven",
            "approximate_length",
            "min_players",
            "max_players",
            "ropecon2018_preferred_time_slots",
            "description",
            "notes_from_host",
        )

        widgets = dict(
            ropecon2018_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2018", slug="roolipeli"),
        )


class LarpForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    """
    LARP form
    """

    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "approximate_length",
            "ropecon2018_sessions",
            "ropecon2018_characters",
            "min_players",
            "description",
            "three_word_description",
            "other_author",
            "ropecon2018_signuplist",
            "ropecon2018_space_requirements",
            "ropecon2018_prop_requirements",
            "ropecon2018_preferred_time_slots",
            "notes_from_host",
            Fieldset(
                _("Whom is the game for?"),
                "is_english_ok",
                "is_age_restricted",
                "is_beginner_friendly",
            ),
        )

        self.fields["title"].help_text = LARP_TITLE_HELP_TEXT

        self.fields["approximate_length"].help_text = LARP_APPROXIMATE_LENGTH_HELP_TEXT

        self.fields["three_word_description"].required = True

        self.fields["description"].required = True
        self.fields["description"].help_text = LARP_DESCRIPTION_HELP_TEXT

        self.fields["min_players"].initial = 6

        self.fields["other_author"].help_text = LARP_OTHER_AUTHOR_HELP_TEXT

        self.fields["ropecon2018_preferred_time_slots"].help_text = LARP_TIMESLOTS_HELP_TEXT

        self.fields["notes_from_host"].help_text = LARP_NOTES_HELP_TEXT

        self.fields["is_english_ok"].help_text = LARP_ENGLISH_OK_HELP_TEXT

        self.fields["is_age_restricted"].help_text = LARP_AGE_RESTRICTED_HELP_TEXT

        self.fields["is_beginner_friendly"].help_text = LARP_BEGINNER_FRIENDLY_HELP_TEXT

    class Meta:
        model = Programme
        fields = (
            "title",
            "approximate_length",
            "ropecon2018_sessions",
            "ropecon2018_characters",
            "min_players",
            "description",
            "three_word_description",
            "other_author",
            "ropecon2018_signuplist",
            "ropecon2018_space_requirements",
            "ropecon2018_prop_requirements",
            "ropecon2018_preferred_time_slots",
            "notes_from_host",
            "is_english_ok",
            "is_age_restricted",
            "is_beginner_friendly",
        )

        widgets = dict(
            ropecon2018_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2018", slug="larp"),
        )


class KorttipeliForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "approximate_length",
            "min_players",
            "max_players",
            "description",
            "three_word_description",
            "ropecon2018_preferred_time_slots",
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

        self.fields["three_word_description"].required = True

        self.fields["description"].help_text = DESCRIPTION_HELP_TEXT
        self.fields["description"].required = True

    class Meta:
        model = Programme
        fields = (
            "title",
            "approximate_length",
            "min_players",
            "max_players",
            "three_word_description",
            "description",
            "ropecon2018_preferred_time_slots",
            "notes_from_host",
            "is_english_ok",
            "is_children_friendly",
            "is_age_restricted",
            "is_beginner_friendly",
            "is_intended_for_experienced_participants",
        )

        widgets = dict(
            ropecon2018_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2018", slug="korttipeli"),
        )


class FigupeliForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "approximate_length",
            "min_players",
            "max_players",
            "description",
            "three_word_description",
            "ropecon2018_preferred_time_slots",
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

        self.fields["three_word_description"].required = True

        self.fields["description"].help_text = DESCRIPTION_HELP_TEXT
        self.fields["description"].required = True

    class Meta:
        model = Programme
        fields = (
            "title",
            "approximate_length",
            "min_players",
            "max_players",
            "three_word_description",
            "description",
            "ropecon2018_preferred_time_slots",
            "notes_from_host",
            "is_english_ok",
            "is_children_friendly",
            "is_age_restricted",
            "is_beginner_friendly",
            "is_intended_for_experienced_participants",
        )

        widgets = dict(
            ropecon2018_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2018", slug="figupeli"),
        )


class KokemuspisteForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "description",
            "three_word_description",
            "ropecon2018_preferred_time_slots",
            "ropecon2018_kp_length",
            "ropecon2018_kp_difficulty",
            "ropecon2018_kp_tables",
            "notes_from_host",
            Fieldset(
                _("Whom is the game for?"),
                "is_english_ok",
                "is_children_friendly",
            ),
        )

        self.fields["three_word_description"].required = True

        self.fields["description"].help_text = DESCRIPTION_HELP_TEXT
        self.fields["description"].required = True

    class Meta:
        model = Programme
        fields = (
            "title",
            "three_word_description",
            "description",
            "ropecon2018_preferred_time_slots",
            "ropecon2018_kp_length",
            "ropecon2018_kp_difficulty",
            "ropecon2018_kp_tables",
            "notes_from_host",
            "is_english_ok",
            "is_children_friendly",
        )

        widgets = dict(
            ropecon2018_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2018", slug="kokemuspiste"),
        )


class LautapeliForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "approximate_length",
            "min_players",
            "max_players",
            "description",
            "three_word_description",
            "ropecon2018_preferred_time_slots",
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

        self.fields["three_word_description"].required = True

        self.fields["description"].help_text = DESCRIPTION_HELP_TEXT
        self.fields["description"].required = True

    class Meta:
        model = Programme
        fields = (
            "title",
            "approximate_length",
            "min_players",
            "max_players",
            "three_word_description",
            "description",
            "ropecon2018_preferred_time_slots",
            "notes_from_host",
            "is_english_ok",
            "is_children_friendly",
            "is_age_restricted",
            "is_beginner_friendly",
            "is_intended_for_experienced_participants",
        )

        widgets = dict(
            ropecon2018_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2018", slug="lautapeli"),
        )


class PuheohjelmaForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "description",
            "category",
            "approximate_length",
            "is_english_ok",
            "is_children_friendly",
            "is_beginner_friendly",
            "ropecon2018_is_no_language",
            "ropecon2018_audience_size",
            "notes_from_host",
            "ropecon2018_is_panel_attendance_ok",
            "ropecon2018_speciality",
            "video_permission",
        )

        self.fields["approximate_length"].help_text = TALK_APPROXIMATE_LENGTH_HELP_TEXT

        self.fields["description"].help_text = TALK_DESCRIPTION_HELP_TEXT
        self.fields["description"].required = True

        self.fields["approximate_length"].initial = 105

        self.fields["ropecon2018_audience_size"].required = False
        self.fields["ropecon2018_is_panel_attendance_ok"].required = False
        self.fields["ropecon2018_speciality"].required = False

        self.fields["category"].queryset = Category.objects.filter(event__slug="ropecon2018", slug__iregex=r"^puhe.+")

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "category",
            "approximate_length",
            "is_english_ok",
            "is_children_friendly",
            "is_beginner_friendly",
            "ropecon2018_is_no_language",
            "ropecon2018_audience_size",
            "notes_from_host",
            "ropecon2018_is_panel_attendance_ok",
            "ropecon2018_speciality",
            "video_permission",
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2018", slug="puheohjelma"),
        )
