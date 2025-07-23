from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from kompassi.core.forms import horizontal_form_helper
from kompassi.core.utils.form_utils import RenderTemplate
from kompassi.labour.forms import AlternativeFormMixin, SignupForm
from kompassi.labour.models import JobCategory, Signup
from kompassi.zombies.programme.forms import AlternativeProgrammeFormMixin
from kompassi.zombies.programme.models import Category, Programme

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
                "certificate_delivery_address",
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
            "certificate_delivery_address",
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

    def clean_certificate_delivery_address(self):
        want_certificate = self.cleaned_data["want_certificate"]
        certificate_delivery_address = self.cleaned_data["certificate_delivery_address"]

        if want_certificate and not certificate_delivery_address:
            raise forms.ValidationError(
                "Koska olet valinnut haluavasi työtodistuksen, on työtodistuksen toimitusosoite täytettävä."
            )

        return certificate_delivery_address


class ProgrammeSignupExtraForm(AlternativeFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = SignupExtra
        fields = (
            "special_diet",
            "special_diet_other",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )


RPG_FORM_FIELD_TEXTS = dict(
    title=(_("Title of your game"), None),
    rpg_system=(_("RPG system"), _("What role-playing game system is used?")),
    approximate_length=(_("Estimated duration of your game (minutes)"), None),
    min_players=(
        _("Minimum number of players"),
        _(
            "Consider the minimum number of players required to run your game carefully: by setting it as low as possible, you increase the chances of your game being able to be run."
        ),
    ),
    max_players=(_("Maximum number of players"), None),
    is_revolving_door=(
        _("Revolving door RPG"),
        _(
            "If new players can join your game while it is already running and old players can leave freely before the game has ended, please tick this box. Mention this in the description of your game as well, and provide additional information in the Comments section below if needed. If you are not sure whether your game is a revolving door RPG or not, contact us and we will figure it out together!"
        ),
    ),
    ropecon_theme=(
        _("Theme: Past and Future"),
        _("If your programme is related to the theme of Ropecon 2023, please tick this box."),
    ),
    ropecon2018_style_serious=(_("Serious playstyle"), None),
    ropecon2018_style_light=(_("Lighthearted playstyle"), None),
    ropecon2018_style_rules_heavy=(_("Rules-heavy"), None),
    ropecon2018_style_rules_light=(_("Rules-light"), None),
    ropecon2018_style_story_driven=(_("Story-driven"), None),
    ropecon2018_style_character_driven=(_("Character-driven"), None),
    ropecon2018_style_combat_driven=(_("Combat-driven"), None),
    description=(
        _("Description of your game"),
        _(
            "Advertise your game for potential players. If your game includes any potentially shocking or distressing themes, please mention it here.<br><br>Recommended length for descriptions is 300-500 characters. We reserve the right to edit and condense the description and the title if necessary.<br><br>Write the description in the language the game will be run in (Finnish, English). You can write the description in both languages if you want."
        ),
    ),
    three_word_description=(
        _("Slogan for your game"),
        _(
            "Condense the essence of your game into one short sentence that will let players know what your game have to offer. For example, “A traditional D&D dungeon crawl”, or “Lovecraftian horror in Equestria”. We reserve the right to edit the slogan if necessary."
        ),
    ),
    ropecon2023_blocked_time_slots=(
        _("When are you NOT able to run your game?"),
        _(
            "Select the times when you are <b>NOT able</b> to run your game. If you have a more specific request in mind regarding your schedule (for example, you would like to run your game late at night), please let us know in the Comments section below.<br/>In this section, we would like to know more about how work or volunteer shifts, public transport schedules and other factors might be impacting your schedule. For example, if you need to leave the venue by 11pm to be able to catch the last bus to your accommodation."
        ),
    ),
    notes_from_host=(
        _("Comments"),
        _(
            "Is there anything else you would like to tell the RPG coordinators that doesn’t fit any of the fields above or would you like to clarify something?<br/>For example, if you are a beginner GM and would like some additional support, let us know and we will gladly help you out!"
        ),
    ),
    photography=(
        _("Programme photography"),
        _(
            "The official photographers of Ropecon aim to take pictures at those programme events they have been requested to take photos of."
        ),
    ),
)


class RpgForm(AlternativeProgrammeFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "title",
            "rpg_system",
            "approximate_length",
            "min_players",
            "max_players",
            "is_revolving_door",
            Fieldset(
                _("Playstyle and mechanics of your game (Choose any which apply)"),
                "ropecon2018_style_serious",
                "ropecon2018_style_light",
                "ropecon2018_style_rules_heavy",
                "ropecon2018_style_rules_light",
                "ropecon2018_style_story_driven",
                "ropecon2018_style_character_driven",
                "ropecon2018_style_combat_driven",
                "description",
                "three_word_description",
                "ropecon2023_blocked_time_slots",
                "notes_from_host",
            ),
            Fieldset(
                _("Who is your programme for?"),
                "ropecon2023_language",
                "ropecon2023_suitable_for_all_ages",
                "ropecon2023_aimed_at_children_under_13",
                "ropecon2023_aimed_at_children_between_13_17",
                "ropecon2023_aimed_at_adult_attendees",
                "ropecon2023_for_18_plus_only",
                "ropecon2023_beginner_friendly",
                "ropecon_theme",
                "ropecon2023_celebratory_year",
                "photography",
            ),
            Fieldset(
                _("Accessibility and inclusivity"),
                RenderTemplate("ropecon2023_rpg_form_accessibility.html"),
                "ropecon2023_accessibility_cant_use_mic",
                "ropecon2021_accessibility_loud_sounds",
                "ropecon2021_accessibility_flashing_lights",
                "ropecon2021_accessibility_strong_smells",
                "ropecon2021_accessibility_irritate_skin",
                "ropecon2021_accessibility_physical_contact",
                "ropecon2021_accessibility_low_lightning",
                "ropecon2021_accessibility_moving_around",
                "ropecon2023_accessibility_programme_duration_over_2_hours",
                "ropecon2023_accessibility_limited_opportunities_to_move_around",
                "ropecon2021_accessibility_video",
                "ropecon2021_accessibility_recording",
                "ropecon2023_accessibility_long_texts",
                "ropecon2023_accessibility_texts_not_available_as_recordings",
                "ropecon2023_accessibility_participation_requires_dexterity",
                "ropecon2023_accessibility_participation_requires_react_quickly",
                "ropecon2021_accessibility_colourblind",
                "ropecon2022_content_warnings",
                "ropecon2023_other_accessibility_information",
            ),
        )

        for field_name, texts in RPG_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

        self.fields["rpg_system"].required = True
        self.fields["approximate_length"].required = True
        self.fields["min_players"].required = True
        self.fields["min_players"].initial = 2
        self.fields["max_players"].required = True
        self.fields["max_players"].initial = 5
        self.fields["description"].required = True
        self.fields["three_word_description"].required = True
        self.fields["ropecon2023_blocked_time_slots"].required = True
        self.fields["photography"].choices = [
            ("please", _("Please photograph my programme")),
            ("okay", _("My programme can be photographed")),
            ("nope", _("I request my programme to not be photographed")),
        ]
        self.fields["photography"].initial = "okay"

    class Meta:
        model = Programme
        fields = [
            "title",
            "rpg_system",
            "approximate_length",
            "min_players",
            "max_players",
            "is_revolving_door",
            "ropecon2018_style_serious",
            "ropecon2018_style_light",
            "ropecon2018_style_rules_heavy",
            "ropecon2018_style_rules_light",
            "ropecon2018_style_story_driven",
            "ropecon2018_style_character_driven",
            "ropecon2018_style_combat_driven",
            "description",
            "three_word_description",
            "ropecon2023_blocked_time_slots",
            "notes_from_host",
            "ropecon2023_language",
            "ropecon2023_suitable_for_all_ages",
            "ropecon2023_aimed_at_children_under_13",
            "ropecon2023_aimed_at_children_between_13_17",
            "ropecon2023_aimed_at_adult_attendees",
            "ropecon2023_for_18_plus_only",
            "ropecon2023_beginner_friendly",
            "ropecon_theme",
            "ropecon2023_celebratory_year",
            "photography",
            "ropecon2023_accessibility_cant_use_mic",
            "ropecon2021_accessibility_loud_sounds",
            "ropecon2021_accessibility_flashing_lights",
            "ropecon2021_accessibility_strong_smells",
            "ropecon2021_accessibility_irritate_skin",
            "ropecon2021_accessibility_physical_contact",
            "ropecon2021_accessibility_low_lightning",
            "ropecon2021_accessibility_moving_around",
            "ropecon2023_accessibility_programme_duration_over_2_hours",
            "ropecon2023_accessibility_limited_opportunities_to_move_around",
            "ropecon2021_accessibility_video",
            "ropecon2021_accessibility_recording",
            "ropecon2023_accessibility_long_texts",
            "ropecon2023_accessibility_texts_not_available_as_recordings",
            "ropecon2023_accessibility_participation_requires_dexterity",
            "ropecon2023_accessibility_participation_requires_react_quickly",
            "ropecon2021_accessibility_colourblind",
            "ropecon2022_content_warnings",
            "ropecon2023_other_accessibility_information",
        ]

        widgets = dict(
            ropecon2023_blocked_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2023", slug="rpg"),
        )


LARP_FORM_FIELD_TEXTS = dict(
    title=(
        _("Title of your larp"),
        _("Give your larp a catchy and concise title. We reserve the right to edit the title if necessary."),
    ),
    approximate_length=(
        _("Estimated duration (minutes)"),
        _("This includes time for propping, brief and debrief, as well as the actual game."),
    ),
    ropecon2018_sessions=(
        _("Number of runs"),
        _(
            "Tell us how many times you would like to run your larp during the convention. Due to limited space we may not be able to fulfill all requests."
        ),
    ),
    ropecon2018_characters=(
        _("Number of characters"),
        _(
            "If the design of your larp requires gendered characters, please mention it in the Comments section of this form."
        ),
    ),
    min_players=(_("Minimum number of players"), _("How many players must sign up for the larp to be able to run it?")),
    description=(
        _("Description"),
        _(
            "Advertise your larp for potential players. Inform players about what is expected of them, and what themes your larp contains. If your larp includes any heavy themes, such as physical violence or psychological abuse, please mention it here.<br/><br/>Recommended length for descriptions is 300-500 characters. We reserve the right to edit and condense the description and the title if necessary."
        ),
    ),
    other_author=(
        _("Game designer (if other than GM)"),
        _(
            "If the larp was designed by someone other than the GM running it at Ropecon, please enter the name of the designer here."
        ),
    ),
    ropecon2018_signuplist=(
        _("Who makes the sign-up list - you or the Larp Desk?"),
        _(
            'If you make the sign-up list for your larp yourself, you can ask more specific questions about player preferences. A sign-up list made by the Larp Desk is simply a list of names. In this case, select "Larp Desk makes the list".'
        ),
    ),
    ropecon2023_blocked_time_slots=(
        _("When are you NOT able to run your larp?"),
        _(
            "Select the times when you are <b>NOT able</b> to run your larp. In other words, leave the times that you would be <b>able</b> to run your larp unselected!<br><br>In this section, we would like to know more about how work or volunteer shifts, public transport schedules and other factors might be impacting your schedule. For example, if you need to leave the venue by 11pm to be able to catch the last bus to your accommodation.<br/><br/>If you have a more specific request in mind regarding your schedule (for example, you would like to run your larp late at night), please let us know in the Comments section below."
        ),
    ),
    notes_from_host=(
        _("Comments"),
        _(
            "Do you want to say something to the larp-conittee that does not fit any of the fields above or clarify some answer?<br/><br/>If the design of your larp requires a large number of your characters to be gendered (for example, a larp about a sauna night with the guys, or about female pilots in WWII).<br/><br/>When deciding which larps to include at Ropecon, we want as many larps as possible to be accessible for as many attendees as possible, regardless of their gender or the gender they prefer to larp as. Requiring a large number of your characters to be gendered may affect whether or not your submission for a larp is accepted.<br/><br/>You can also specify your preferred schedule here."
        ),
    ),
    ropecon_theme=(
        _("Theme: Past and Future"),
        _("If your programme is related to the theme of Ropecon 2023, please tick this box."),
    ),
    ropecon2018_space_requirements=(
        _("Space and technical needs"),
        _(
            "Describe what kind of space you hope to organise your larp in (completely dark, separate rooms, water supply, etc.) and whether you have any technical needs (lights, sound, etc). Please keep in mind that we may not be able to fulfill all requests, so please justify how yours would benefit your larp."
        ),
    ),
    ropecon2018_prop_requirements=(
        _("Equipment needed in your larp"),
        _(
            "Tell us what kind of equipment or props are required in your larp and which of them you can provide yourself. Please keep in mind that due to limited resources we are not able to fulfill the most outlandish of requests. Water and cups will be provided for all larps."
        ),
    ),
    photography=(
        _("Programme photography"),
        _(
            "The official photographers of Ropecon aim to take pictures at those programme events they have been requested to take photos of."
        ),
    ),
)


class LarpForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "other_author",
            "approximate_length",
            "ropecon2018_sessions",
            "ropecon2018_characters",
            "min_players",
            "description",
            Fieldset(
                _("Practicalities"),
                "ropecon2018_signuplist",
                "ropecon2018_space_requirements",
                "ropecon2018_prop_requirements",
                "ropecon2023_blocked_time_slots",
                "notes_from_host",
            ),
            Fieldset(
                _("Who is your programme for?"),
                "ropecon2023_language",
                "ropecon2023_suitable_for_all_ages",
                "ropecon2023_aimed_at_children_under_13",
                "ropecon2023_aimed_at_children_between_13_17",
                "ropecon2023_aimed_at_adult_attendees",
                "ropecon2023_for_18_plus_only",
                "ropecon2023_beginner_friendly",
                "ropecon_theme",
                "ropecon2023_celebratory_year",
                "photography",
            ),
            Fieldset(
                _("Accessibility and inclusivity"),
                RenderTemplate("ropecon2023_larp_form_accessibility.html"),
                "ropecon2021_accessibility_loud_sounds",
                "ropecon2021_accessibility_flashing_lights",
                "ropecon2021_accessibility_strong_smells",
                "ropecon2021_accessibility_irritate_skin",
                "ropecon2021_accessibility_physical_contact",
                "ropecon2021_accessibility_low_lightning",
                "ropecon2021_accessibility_moving_around",
                "ropecon2023_accessibility_programme_duration_over_2_hours",
                "ropecon2023_accessibility_limited_opportunities_to_move_around",
                "ropecon2021_accessibility_video",
                "ropecon2021_accessibility_recording",
                "ropecon2023_accessibility_long_texts",
                "ropecon2023_accessibility_texts_not_available_as_recordings",
                "ropecon2023_accessibility_participation_requires_dexterity",
                "ropecon2023_accessibility_participation_requires_react_quickly",
                "ropecon2021_accessibility_colourblind",
                "ropecon2022_content_warnings",
                "ropecon2023_other_accessibility_information",
            ),
        )

        for field_name, texts in LARP_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

        self.fields["ropecon2018_sessions"].initial = 2
        self.fields["ropecon2018_characters"].initial = 10
        self.fields["min_players"].required = True
        self.fields["min_players"].initial = 6
        self.fields["description"].required = True
        self.fields["ropecon2018_signuplist"].choices = [
            ("none", _("No sign-up")),
            ("tiski", _("The Larp Desk will make the sign-up list")),
            ("itse", _("I will make my own sign-up list")),
        ]
        self.fields["ropecon2018_signuplist"].choices = [
            (k, t) for (k, t) in self.fields["ropecon2018_signuplist"].choices if k != "none"
        ]
        self.fields["ropecon2023_blocked_time_slots"].required = True
        self.fields["photography"].choices = [
            ("please", _("Please photograph my programme")),
            ("okay", _("My programme can be photographed")),
            ("nope", _("I request my programme to not be photographed")),
        ]
        self.fields["photography"].initial = "okay"

    class Meta:
        model = Programme
        fields = (
            "title",
            "other_author",
            "approximate_length",
            "ropecon2018_sessions",
            "ropecon2018_characters",
            "min_players",
            "description",
            "ropecon2018_signuplist",
            "ropecon2018_space_requirements",
            "ropecon2018_prop_requirements",
            "ropecon2023_blocked_time_slots",
            "notes_from_host",
            "ropecon2023_language",
            "ropecon2023_suitable_for_all_ages",
            "ropecon2023_aimed_at_children_under_13",
            "ropecon2023_aimed_at_children_between_13_17",
            "ropecon2023_aimed_at_adult_attendees",
            "ropecon2023_for_18_plus_only",
            "ropecon2023_beginner_friendly",
            "ropecon_theme",
            "ropecon2023_celebratory_year",
            "photography",
            "ropecon2021_accessibility_loud_sounds",
            "ropecon2021_accessibility_flashing_lights",
            "ropecon2021_accessibility_strong_smells",
            "ropecon2021_accessibility_irritate_skin",
            "ropecon2021_accessibility_physical_contact",
            "ropecon2021_accessibility_low_lightning",
            "ropecon2021_accessibility_moving_around",
            "ropecon2023_accessibility_programme_duration_over_2_hours",
            "ropecon2023_accessibility_limited_opportunities_to_move_around",
            "ropecon2021_accessibility_video",
            "ropecon2021_accessibility_recording",
            "ropecon2023_accessibility_long_texts",
            "ropecon2023_accessibility_texts_not_available_as_recordings",
            "ropecon2023_accessibility_participation_requires_dexterity",
            "ropecon2023_accessibility_participation_requires_react_quickly",
            "ropecon2021_accessibility_colourblind",
            "ropecon2022_content_warnings",
            "ropecon2023_other_accessibility_information",
        )

        widgets = dict(
            content_warnings=forms.Textarea,
            ropecon2023_blocked_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2023", slug="larp"),
        )


PROGRAMME_FORM_FIELD_TEXTS = dict(
    title=(
        _("Title of your programme"),
        _(
            "Come up with a catchy, concise title for your programme. Ropecon reserves the right to edit the title if necessary."
        ),
    ),
    description=(
        _("Description"),
        _(
            "Describe your programme to your potential audience or participants in an appealing way. If your programme contains topics or themes that are heavy or potentially distressing, please pay special attention to those in the description. If your programme is meant as humorous or entertaining in nature, let it show in the description as well. Recommended length is 300-500 characters. Ropecon reserves the right to edit and condense the description and title of the programme if necessary."
        ),
    ),
    category=(
        _("Programme category"),
        _(
            "Choose the category that best suits your programme. Ropecon reserves the right to change the programme category if necessary.<br/>Presentation: traditional lecture<br/>Panel discussion: multiple panelists in front of an audience, usually with a moderator present<br/>Discussion group: discussion that equally includes the audience<br/>Dance programme: dance rehearsals and for example a ball; dance programmes where attendees also dance<br/>Performance programme: all types of performances; choir, dance performance, fencing performance or other<br/>Meetup: informal gathering related to a certain topic or scene<br/>Other programme: programmes that do not fit the previous categories"
        ),
    ),
    approximate_length=(
        _("Estimated duration (minutes)"),
        _(
            "Duration of presentations, panel discussions and other similar programme is either 45 minutes or 105 minutes (one hour and 45 minutes)."
        ),
    ),
    ropecon2023_language=(
        _("Choose the language used in your programme"),
        _(
            "Finnish - choose this, if only Finnish is spoken in your programme.<br/>English - choose this, if only English is spoken in your programme.<br/>Language-free - choose this, if no Finnish or English is necessary to participate in the programme (e.g. a workshop with picture instructions or a dance where one can follow what others are doing).<br/>Finnish or English - choose this, if you are okay with either of the two languages. The programme team will contact you regarding the final choice of language."
        ),
    ),
    ropecon_theme=(
        _("Theme: Past and Future"),
        _("If your programme is related to the theme of Ropecon 2023, please tick this box."),
    ),
    max_players=(
        _("Number of participants"),
        _(
            "If the number of participants in your programme is limited, please provide the maximum number of participants."
        ),
    ),
    computer=(
        _("Laptop needs"),
        _(
            "What kind of a laptop will you use? We strongly recommend using a laptop provided by Ropecon. Using your own laptop is possible only when notified in advance."
        ),
    ),
    tech_requirements=(_("Other technical needs"), None),
    ropecon2023_blocked_time_slots=(
        _("When are you NOT able to host your programme?"),
        _(
            "Select the times when you <b>DO NOT</b> want to host your programme. Time slots have been intentionally left vague. If you have a more specific request in mind regarding your schedule, please let us know in the Comments section below."
        ),
    ),
    notes_from_host=(
        _("Comments"),
        _("Is there anything else you would like to tell the programme coordinators or organisers of Ropecon?"),
    ),
    is_available_for_panel=(
        _("Panel discussions"),
        _("I'm interested in participating in a panel discussion related to my field(s) of expertise."),
    ),
    field_of_expertise=(_("My field(s) of expertise"), None),
    video_permission=(
        _("Recording & publishing consent"),
        _("Do you give Ropecon permission to record your programme and publish it on the Internet?"),
    ),
    photography=(
        _("Programme photography"),
        _(
            "The official photographers of Ropecon aim to take pictures at those programme events they have been requested to take photos of."
        ),
    ),
)


class ProgrammeForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "description",
            "category",
            "approximate_length",
            "ropecon2023_language",
            "ropecon2023_suitable_for_all_ages",
            "ropecon2023_aimed_at_children_under_13",
            "ropecon2023_aimed_at_children_between_13_17",
            "ropecon2023_aimed_at_adult_attendees",
            "ropecon2023_for_18_plus_only",
            "ropecon2023_beginner_friendly",
            "ropecon_theme",
            "ropecon2023_celebratory_year",
            "max_players",
            "computer",
            "tech_requirements",
            "ropecon2023_blocked_time_slots",
            "notes_from_host",
            "is_available_for_panel",
            "field_of_expertise",
            "video_permission",
            "photography",
            Fieldset(
                _("Accessibility and inclusivity"),
                RenderTemplate("ropecon2023_programme_form_accessibility.html"),
                "ropecon2023_accessibility_cant_use_mic",
                "ropecon2021_accessibility_loud_sounds",
                "ropecon2021_accessibility_flashing_lights",
                "ropecon2021_accessibility_strong_smells",
                "ropecon2021_accessibility_irritate_skin",
                "ropecon2021_accessibility_physical_contact",
                "ropecon2021_accessibility_low_lightning",
                "ropecon2021_accessibility_moving_around",
                "ropecon2023_accessibility_programme_duration_over_2_hours",
                "ropecon2021_accessibility_video",
                "ropecon2021_accessibility_recording",
                "ropecon2023_accessibility_long_texts",
                "ropecon2023_accessibility_texts_not_available_as_recordings",
                "ropecon2021_accessibility_colourblind",
                "ropecon2022_content_warnings",
                "ropecon2023_other_accessibility_information",
            ),
        )

        for field_name, texts in PROGRAMME_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

        self.fields["description"].required = True
        self.fields["approximate_length"].required = True
        self.fields["video_permission"].required = True
        self.fields["approximate_length"].initial = 45

        self.fields["category"].queryset = Category.objects.filter(
            event=event,
            slug__in=(
                "pres",
                "panel",
                "disc",
                "dance",
                "perforprog",
                "meetup",
                "other",
            ),
        )
        self.fields["computer"].choices = [
            ("con", _("Laptop provided by Ropecon")),
            ("pc", _("Own laptop (PC)")),
            ("mac", _("Own laptop (Mac)")),
            ("none", _("No laptop is needed in my programme")),
        ]
        self.fields["ropecon2023_blocked_time_slots"].required = True
        self.fields["video_permission"].choices = [
            ("public", _("I give permission to record and publish my programme")),
            ("forbidden", _("I do not give permission to record or publish my programme")),
        ]
        self.fields["video_permission"].blank = True
        self.fields["photography"].choices = [
            ("please", _("Please photograph my programme")),
            ("okay", _("My programme can be photographed")),
            ("nope", _("I request my programme to not be photographed")),
        ]
        self.fields["photography"].initial = "okay"

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "category",
            "approximate_length",
            "ropecon2023_language",
            "ropecon2023_suitable_for_all_ages",
            "ropecon2023_aimed_at_children_under_13",
            "ropecon2023_aimed_at_children_between_13_17",
            "ropecon2023_aimed_at_adult_attendees",
            "ropecon2023_for_18_plus_only",
            "ropecon2023_beginner_friendly",
            "ropecon_theme",
            "ropecon2023_celebratory_year",
            "max_players",
            "computer",
            "tech_requirements",
            "ropecon2023_blocked_time_slots",
            "notes_from_host",
            "is_available_for_panel",
            "field_of_expertise",
            "video_permission",
            "photography",
            "ropecon2023_accessibility_cant_use_mic",
            "ropecon2021_accessibility_loud_sounds",
            "ropecon2021_accessibility_flashing_lights",
            "ropecon2021_accessibility_strong_smells",
            "ropecon2021_accessibility_irritate_skin",
            "ropecon2021_accessibility_physical_contact",
            "ropecon2021_accessibility_low_lightning",
            "ropecon2021_accessibility_moving_around",
            "ropecon2023_accessibility_programme_duration_over_2_hours",
            "ropecon2021_accessibility_video",
            "ropecon2021_accessibility_recording",
            "ropecon2023_accessibility_long_texts",
            "ropecon2023_accessibility_texts_not_available_as_recordings",
            "ropecon2021_accessibility_colourblind",
            "ropecon2022_content_warnings",
            "ropecon2023_other_accessibility_information",
        )

        widgets = dict(
            ropecon2023_blocked_time_slots=forms.CheckboxSelectMultiple,
        )


GAMING_DESK_FORM_FIELD_TEXTS = dict(
    title=(
        _("Title of your game programme"),
        _(
            "Come up with a catchy, concise title for your game programme. Ropecon reserves the right to edit the title if necessary.<br/>Write the title of the game programme in the language the game will be played in (Finnish or English). You can also write the title in both languages, if you prefer."
        ),
    ),
    description=(
        _("Description"),
        _(
            "Describe your game programme to your potential players in an appealing way. Inform players what is expected of them and what themes your game contains. If your game programme contains topics or themes that are heavy or potentially distressing, please pay special attention to those in the description. If your game programme is meant as humorous or entertaining in nature, let it show in the description as well.<br/>Recommended length is 300-500 characters. Ropecon reserves the right to edit and condense the description and title of the game programme if necessary.<br/>Write the description of the game programme in the language the game will be played in (Finnish or English). You can also write the description in both languages, if you prefer."
        ),
    ),
    category=(
        _("Category of the game programme"),
        _(
            "Choose the category that best suits your game programme. Ropecon reserves the right to change the programme category if necessary.<br/>Experience Point - Demo games (i.e. showcasing, demonstrating or running a game) and open games (i.e. running a certain card game or board game for attendees by request) organized at the Experience Point.<br/>Miniature wargames - demonstrations and open games organized at the miniature wargame area.<br/>Tournaments - organizing a game tournament or a competition at the tournament area or the miniature wargame area.<br/>Other game programme - something other than mentioned above, e.g. jigsaw puzzles."
        ),
    ),
    approximate_length=(
        _("Estimated duration (minutes)"),
        _(
            "Please make an estimation for the duration of your game programme.<br/>For game programme held at the Experience Point, shorter games of 1-3 hours (60-180 min) are preferred."
        ),
    ),
    min_players=(
        _("Minimum number of players"),
        _(
            "How many players are needed for the game programe to be organized?<br/>Select the minimum number of players carefully: by setting the minimum number of players as low as possible, you maximize the chances for your game programme to be organized successfully."
        ),
    ),
    max_players=(
        _("Maximum number of players"),
        _(
            "If the maximum number of players in your game programme is limited, please set the maximum number of players that can participate at the same time."
        ),
    ),
    rpg_system=(
        _("Game system"),
        _(
            'What game system is used in your game programme? For example, "Magic the Gathering" or "Carcassonne".<br/>If you designed the game system yourself, describe it in a few words. For example, "4X, space battle, conquest"'
        ),
    ),
    ropecon2020_materials_language=(
        _("Language used in game materials"),
        _("What language is used in the game materials offered for attendees?"),
    ),
    ropecon2021_gamedesk_materials=(
        _("Does your programme require materials from the players?"),
        _(
            "Specify here whether the attendees participating in your game programme are expected to bring their own game tools or other equipment for the game and what that equipment is (e.g. card decks, figure armies)."
        ),
    ),
    tech_requirements=(
        _("Space and technical needs"),
        _(
            "Does your game programme have any technical needs (e.g. electricity) or other specific needs regarding e.g. the programme space itself?<br/>Please keep in mind that we might not be able to fulfill all requests, so please justify how your requests would benefit your game programme."
        ),
    ),
    ropecon2023_blocked_time_slots=(
        _("When are you NOT able to host your game programme?"),
        _(
            "Select the times when you are <b>NOT able</b> to organize your game programme.<br/><br/>Time slots have been intentionally left vague. If you have a more specific request in mind regarding your schedule, please let us know in the Comments section below."
        ),
    ),
    notes_from_host=(
        _("Comments"),
        _("Is there anything else you would like to tell the game programme coordinators?"),
    ),
    is_available_for_panel=(
        _("Panel discussions"),
        _("I'm interested in participating in a panel discussion related to my field(s) of expertise."),
    ),
    field_of_expertise=(_("My field(s) of expertise"), None),
    photography=(
        _("Programme photography"),
        _(
            "The official photographers of Ropecon aim to take pictures at those programme events they have been requested to take photos of."
        ),
    ),
    ropecon_theme=(
        _("Theme: Past and Future"),
        _("If your programme is related to the theme of Ropecon 2023, please tick this box."),
    ),
)


class GamingDeskForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "description",
            "category",
            "approximate_length",
            "min_players",
            "max_players",
            "rpg_system",
            "ropecon2020_materials_language",
            "ropecon2021_gamedesk_materials",
            "ropecon2023_signuplist",
            "ropecon2023_tables",
            "ropecon2023_chairs",
            "tech_requirements",
            "ropecon2023_blocked_time_slots",
            "notes_from_host",
            "is_available_for_panel",
            "field_of_expertise",
            "photography",
            Fieldset(
                _("Who is your programme for?"),
                "ropecon2023_language",
                "ropecon2023_suitable_for_all_ages",
                "ropecon2023_aimed_at_children_under_13",
                "ropecon2023_aimed_at_children_between_13_17",
                "ropecon2023_aimed_at_adult_attendees",
                "ropecon2023_for_18_plus_only",
                "ropecon2023_beginner_friendly",
                "ropecon_theme",
                "ropecon2023_celebratory_year",
            ),
            Fieldset(
                _("Accessibility and inclusivity"),
                RenderTemplate("ropecon2023_gamedesk_form_accessibility.html"),
                "ropecon2023_accessibility_cant_use_mic",
                "ropecon2021_accessibility_loud_sounds",
                "ropecon2021_accessibility_flashing_lights",
                "ropecon2021_accessibility_physical_contact",
                "ropecon2023_accessibility_programme_duration_over_2_hours",
                "ropecon2023_accessibility_limited_opportunities_to_move_around",
                "ropecon2021_accessibility_recording",
                "ropecon2023_accessibility_long_texts",
                "ropecon2023_accessibility_texts_not_available_as_recordings",
                "ropecon2023_accessibility_participation_requires_dexterity",
                "ropecon2023_accessibility_participation_requires_react_quickly",
                "ropecon2021_accessibility_colourblind",
                "ropecon2022_content_warnings",
                "ropecon2023_other_accessibility_information",
            ),
        )

        for field_name, texts in GAMING_DESK_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

        self.fields["category"].queryset = Category.objects.filter(
            event=event,
            slug__in=(
                "expdemo",
                "expopen",
                "expother",
                "minidemo",
                "miniopen",
                "tourmini",
                "tourcard",
                "tourboard",
                "tourother",
                "othergame",
            ),
        )
        self.fields["approximate_length"].required = True
        self.fields["approximate_length"].initial = 180
        self.fields["min_players"].required = True
        self.fields["min_players"].initial = False
        self.fields["description"].required = True
        self.fields["ropecon2023_tables"].required = True
        self.fields["ropecon2023_chairs"].required = True
        self.fields["ropecon2023_blocked_time_slots"].required = True
        self.fields["photography"].choices = [
            ("please", _("Please photograph my programme")),
            ("okay", _("My programme can be photographed")),
            ("nope", _("I request my programme to not be photographed")),
        ]
        self.fields["photography"].required = True
        self.fields["photography"].initial = "okay"

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "category",
            "approximate_length",
            "min_players",
            "max_players",
            "rpg_system",
            "ropecon2020_materials_language",
            "ropecon2021_gamedesk_materials",
            "ropecon2023_signuplist",
            "ropecon2023_tables",
            "ropecon2023_chairs",
            "tech_requirements",
            "ropecon2023_blocked_time_slots",
            "notes_from_host",
            "is_available_for_panel",
            "field_of_expertise",
            "photography",
            "ropecon2023_language",
            "ropecon2023_suitable_for_all_ages",
            "ropecon2023_aimed_at_children_under_13",
            "ropecon2023_aimed_at_children_between_13_17",
            "ropecon2023_aimed_at_adult_attendees",
            "ropecon2023_for_18_plus_only",
            "ropecon2023_beginner_friendly",
            "ropecon_theme",
            "ropecon2023_celebratory_year",
            "ropecon2023_accessibility_cant_use_mic",
            "ropecon2021_accessibility_loud_sounds",
            "ropecon2021_accessibility_flashing_lights",
            "ropecon2021_accessibility_physical_contact",
            "ropecon2023_accessibility_programme_duration_over_2_hours",
            "ropecon2023_accessibility_limited_opportunities_to_move_around",
            "ropecon2021_accessibility_recording",
            "ropecon2023_accessibility_long_texts",
            "ropecon2023_accessibility_texts_not_available_as_recordings",
            "ropecon2023_accessibility_participation_requires_dexterity",
            "ropecon2023_accessibility_participation_requires_react_quickly",
            "ropecon2021_accessibility_colourblind",
            "ropecon2022_content_warnings",
            "ropecon2023_other_accessibility_information",
        )

        widgets = dict(
            content_warnings=forms.Textarea,
            ropecon2023_blocked_time_slots=forms.CheckboxSelectMultiple,
        )


WORKSHOP_FORM_FIELD_TEXTS = dict(
    title=(
        _("Title of your programme"),
        _(
            "Come up with a catchy, concise title for your programme. Ropecon reserves the right to edit the title if necessary."
        ),
    ),
    description=(
        _("Description"),
        _(
            "Describe your programme to your potential audience or participants in an appealing way. If your programme contains topics or themes that are heavy or potentially distressing, please pay special attention to those in the description. If your programme is meant as humorous or entertaining in nature, let it show in the description as well. Recommended length is 300-500 characters. Ropecon reserves the right to edit and condense the description and title of the programme if necessary."
        ),
    ),
    category=(
        _("Programme category"),
        _(
            "Choose the category that best suits your programme. Ropecon reserves the right to change the programme category if necessary."
        ),
    ),
    approximate_length=(
        _("Estimated duration (minutes)"),
        _("Duration of workshops is either 45 minutes, 105 minutes or 165 minutes."),
    ),
    ropecon2023_language=(
        _("Choose the language used in your programme"),
        _(
            "Finnish - choose this, if only Finnish is spoken in your programme.<br/>English - choose this, if only English is spoken in your programme.<br/>Language-free - choose this, if no Finnish or English is necessary to participate in the programme (e.g. a workshop with picture instructions or a dance where one can follow what others are doing).<br/>Finnish or English - choose this, if you are okay with either of the two languages. The programme team will contact you regarding the final choice of language."
        ),
    ),
    ropecon_theme=(
        _("Theme: Past and Future"),
        _("If your programme is related to the theme of Ropecon 2023, please tick this box."),
    ),
    max_players=(
        _("Number of participants"),
        _(
            "If the number of participants in your workshop is limited, please provide the maximum number of participants."
        ),
    ),
    computer=(
        _("Laptop needs"),
        _(
            "Will you need a laptop at your workshop? We strongly recommend using a laptop provided by Ropecon. Using your own laptop is possible only when notified in advance."
        ),
    ),
    tech_requirements=(
        _("Other technical needs"),
        _("Inform us about other possible technical needs at your workshop."),
    ),
    ropecon2023_blocked_time_slots=(
        _("When are you NOT able to host your programme?"),
        _(
            "Select the times when you <b>DO NOT</b> want to host your programme. Time slots have been intentionally left vague. If you have a more specific request in mind regarding your schedule, please let us know in the Comments section below."
        ),
    ),
    notes_from_host=(
        _("Comments"),
        _("Is there anything else you would like to tell the programme coordinators or organisers of Ropecon?"),
    ),
    is_available_for_panel=(
        _("Panel discussions"),
        _("I'm interested in participating in a panel discussion related to my field(s) of expertise."),
    ),
    field_of_expertise=(_("My field(s) of expertise"), None),
    photography=(
        _("Programme photography"),
        _(
            "The official photographers of Ropecon aim to take pictures at those programme events they have been requested to take photos of."
        ),
    ),
)


class WorkshopForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        kwargs.pop("admin", False)

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "title",
            "description",
            "category",
            "approximate_length",
            "ropecon2023_language",
            "ropecon2023_suitable_for_all_ages",
            "ropecon2023_aimed_at_children_under_13",
            "ropecon2023_aimed_at_children_between_13_17",
            "ropecon2023_aimed_at_adult_attendees",
            "ropecon2023_for_18_plus_only",
            "ropecon2023_beginner_friendly",
            "ropecon_theme",
            "ropecon2023_celebratory_year",
            "max_players",
            "ropecon2023_workshop_fee",
            "ropecon2023_material_needs",
            "ropecon2023_tables_and_chairs",
            "ropecon2023_furniture_needs",
            "computer",
            "tech_requirements",
            "ropecon2023_blocked_time_slots",
            "notes_from_host",
            "is_available_for_panel",
            "field_of_expertise",
            "photography",
            Fieldset(
                _("Accessibility and inclusivity"),
                RenderTemplate("ropecon2023_programme_form_accessibility.html"),
                "ropecon2023_accessibility_cant_use_mic",
                "ropecon2021_accessibility_loud_sounds",
                "ropecon2021_accessibility_flashing_lights",
                "ropecon2021_accessibility_strong_smells",
                "ropecon2021_accessibility_irritate_skin",
                "ropecon2021_accessibility_physical_contact",
                "ropecon2021_accessibility_low_lightning",
                "ropecon2021_accessibility_moving_around",
                "ropecon2023_accessibility_programme_duration_over_2_hours",
                "ropecon2023_accessibility_limited_opportunities_to_move_around",
                "ropecon2021_accessibility_video",
                "ropecon2021_accessibility_recording",
                "ropecon2023_accessibility_long_texts",
                "ropecon2023_accessibility_texts_not_available_as_recordings",
                "ropecon2023_accessibility_participation_requires_dexterity",
                "ropecon2021_accessibility_colourblind",
                "ropecon2022_content_warnings",
                "ropecon2023_other_accessibility_information",
            ),
        )

        for field_name, texts in WORKSHOP_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

        self.fields["description"].required = True
        self.fields["approximate_length"].required = True
        self.fields["approximate_length"].initial = 105

        self.fields["category"].queryset = Category.objects.filter(
            event=event,
            slug__in=(
                "workcraft",
                "workmini",
                "workmusic",
                "workother",
            ),
        )
        self.fields["ropecon2023_workshop_fee"].required = True
        self.fields["computer"].choices = [
            ("none", _("No laptop is needed in my programme")),
            ("con", _("Laptop provided by Ropecon")),
            ("pc", _("Own laptop (PC)")),
            ("mac", _("Own laptop (Mac)")),
        ]
        self.fields["computer"].initial = "none"
        self.fields["ropecon2023_blocked_time_slots"].required = True
        self.fields["photography"].choices = [
            ("please", _("Please photograph my programme")),
            ("okay", _("My programme can be photographed")),
            ("nope", _("I request my programme to not be photographed")),
        ]
        self.fields["photography"].initial = "okay"

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "category",
            "approximate_length",
            "ropecon2023_language",
            "ropecon2023_suitable_for_all_ages",
            "ropecon2023_aimed_at_children_under_13",
            "ropecon2023_aimed_at_children_between_13_17",
            "ropecon2023_aimed_at_adult_attendees",
            "ropecon2023_for_18_plus_only",
            "ropecon2023_beginner_friendly",
            "ropecon_theme",
            "ropecon2023_celebratory_year",
            "max_players",
            "ropecon2023_workshop_fee",
            "ropecon2023_material_needs",
            "ropecon2023_tables_and_chairs",
            "ropecon2023_furniture_needs",
            "computer",
            "tech_requirements",
            "ropecon2023_blocked_time_slots",
            "notes_from_host",
            "is_available_for_panel",
            "field_of_expertise",
            "photography",
            "ropecon2023_accessibility_cant_use_mic",
            "ropecon2021_accessibility_loud_sounds",
            "ropecon2021_accessibility_flashing_lights",
            "ropecon2021_accessibility_strong_smells",
            "ropecon2021_accessibility_irritate_skin",
            "ropecon2021_accessibility_physical_contact",
            "ropecon2021_accessibility_low_lightning",
            "ropecon2021_accessibility_moving_around",
            "ropecon2023_accessibility_programme_duration_over_2_hours",
            "ropecon2023_accessibility_limited_opportunities_to_move_around",
            "ropecon2021_accessibility_video",
            "ropecon2021_accessibility_recording",
            "ropecon2023_accessibility_long_texts",
            "ropecon2023_accessibility_texts_not_available_as_recordings",
            "ropecon2023_accessibility_participation_requires_dexterity",
            "ropecon2021_accessibility_colourblind",
            "ropecon2022_content_warnings",
            "ropecon2023_other_accessibility_information",
        )

        widgets = dict(
            ropecon2023_blocked_time_slots=forms.CheckboxSelectMultiple,
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
        self.fields["job_title"].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="ropecon2023", name="Conitea"))


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
            roster_publish_consent=True,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict()


class SpecialistSignupForm(SignupForm, AlternativeFormMixin):
    def get_job_categories_query(self, event, admin=False):
        assert not admin

        return Q(event__slug="ropecon2023", name__in=["Boffaus", "Teehuone"])

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
                "certificate_delivery_address",
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
            "certificate_delivery_address",
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
