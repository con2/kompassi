from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from kompassi.core.forms import horizontal_form_helper
from kompassi.labour.forms import AlternativeFormMixin
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
                "can_finnish",
                "can_english",
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

        self.fields["roster_publish_consent"].required = True

    class Meta:
        model = SignupExtra
        fields = (
            "shift_type",
            "want_certificate",
            "certificate_delivery_address",
            "can_finnish",
            "can_english",
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
    is_in_english=(_("In English"), _("If your game can be run in English, please tick this box.")),
    is_age_restricted=(
        _("For players over 18 only"),
        _(
            "If your game contains themes that require players to be 18 years or older, please tick this box. There will be an ID check for all players."
        ),
    ),
    is_beginner_friendly=(
        _("Beginner-friendly"),
        _(
            "If your game is suitable for players with very limited or without any previous experience about RPGs, please tick this box."
        ),
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
    ropecon2019_blocked_time_slots=(
        _("When are you NOT able to run your game?"),
        _(
            "Select the times when you are NOT able to run your game. If you have a more specific request in mind regarding your schedule (for example, you would like to run your game late at night), please let us know in the Comments section below.<br><br>In this section, we would like to know more about how work or volunteer shifts, public transport schedules and other factors might be impacting your schedule. For example, if you need to leave the venue by 11pm to be able to catch the last bus to your accommodation."
        ),
    ),
    notes_from_host=(
        _("Comments"),
        _(
            "Is there anything else you would like to tell the RPG coordinators? For example, if you are a beginner GM and would like some additional support, let us know and we will gladly help you out!"
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
                _("Who is the game meant for?"),
                "is_in_english",
                "is_age_restricted",
                "ropecon2020_suitable_for_children_under_7",
                "ropecon2020_suitable_for_children_aged_7_12",
                "ropecon2020_suitable_for_children_aged_12_plus",
                "ropecon2020_not_suitable_for_children",
                "is_beginner_friendly",
                "ropecon2020_theme_end_of_the_world",
                "ropecon2020_theme_dinosaurs",
            ),
            Fieldset(
                _("Playstyle and mechanics (Choose any which apply)"),
                "ropecon2018_style_serious",
                "ropecon2018_style_light",
                "ropecon2018_style_rules_heavy",
                "ropecon2018_style_rules_light",
                "ropecon2018_style_story_driven",
                "ropecon2018_style_character_driven",
                "ropecon2018_style_combat_driven",
                "description",
                "three_word_description",
                "ropecon2019_blocked_time_slots",
                "notes_from_host",
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
        self.fields["ropecon2019_blocked_time_slots"].required = True

    class Meta:
        model = Programme
        fields = [
            "title",
            "rpg_system",
            "approximate_length",
            "min_players",
            "max_players",
            "is_revolving_door",
            "is_in_english",
            "is_age_restricted",
            "ropecon2020_suitable_for_children_under_7",
            "ropecon2020_suitable_for_children_aged_7_12",
            "ropecon2020_suitable_for_children_aged_12_plus",
            "ropecon2020_not_suitable_for_children",
            "is_beginner_friendly",
            "ropecon2020_theme_end_of_the_world",
            "ropecon2020_theme_dinosaurs",
            "ropecon2018_style_serious",
            "ropecon2018_style_light",
            "ropecon2018_style_rules_heavy",
            "ropecon2018_style_rules_light",
            "ropecon2018_style_story_driven",
            "ropecon2018_style_character_driven",
            "ropecon2018_style_combat_driven",
            "description",
            "three_word_description",
            "ropecon2019_blocked_time_slots",
            "notes_from_host",
        ]

        widgets = dict(
            ropecon2019_blocked_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2020", slug="rpg"),
        )


LARP_FORM_FIELD_TEXTS = dict(
    title=(
        _("Title of your larp"),
        _("Give your larp a catchy and concise title. We reserve the right to edit the title if necessary."),
    ),
    approximate_length=(
        _("Estimated duration (minutes)"),
        _(
            "For one run of a 3-4 hour original larp (180-240 minutes) you will receive a one-day ticket to Ropecon. This includes time for propping, brief and debrief, as well as the actual game."
        ),
    ),
    ropecon2018_sessions=(
        _("Number of runs"),
        _(
            "Tell us how many times you would like to run your larp during the convention. Due to limited space we may not be able to fulfill all requests.<br><br>For one run of a 3-4 hour original larp or two runs of a pre-written scenario you will receive one weekend ticket as a GM. Additional runs of your larp will yield an extra one-day ticket."
        ),
    ),
    ropecon2018_characters=(
        _("Number of characters"),
        _(
            "If the design of your game requires gendered characters, please mention it in the Comments section of this form."
        ),
    ),
    min_players=(_("Minimum number of players"), _("How many players must sign up for the larp to be able to run it?")),
    description=(
        _("Description"),
        _(
            "Advertise your larp for potential players. Inform players about what is expected of them, and what themes your larp contains. If your larp includes any heavy themes, such as physical violence or psychological abuse, please mention it here.<br><br>Recommended length for descriptions is 300-500 characters. We reserve the right to edit and condense the description and the title if necessary."
        ),
    ),
    content_warnings=(
        _("Content warnings"),
        _(
            "If your larp contains any heavy topics or themes that some players may find distressing, please mention them here."
        ),
    ),
    other_author=(
        _("Game designer (if other than GM)"),
        _(
            "If the game was designed by someone other than the GM running it at Ropecon, please enter the name of the designer here."
        ),
    ),
    ropecon2018_signuplist=(
        _("Who makes the sign-up list - you or the Larp Desk?"),
        _(
            "If you make the sign-up list for your larp yourself, you can ask more specific questions about player preferences. A sign-up list made by the Larp Desk is simply a list of names."
        ),
    ),
    ropecon2019_blocked_time_slots=(
        _("When are you NOT able to run your game?"),
        _(
            "Select the times when you are NOT able to run your larp. In other words, leave the times that you would be able to run your larp unselected!<br><br>If you have a more specific request in mind regarding your schedule (for example, you would like to run your larp late at night), please let us know in the Comments section below.<br><br>In this section, we would like to know more about how work or volunteer shifts, public transport schedules and other factors might be impacting your schedule. For example, if you need to leave the venue by 11pm to be able to catch the last bus to your accommodation."
        ),
    ),
    notes_from_host=(
        _("Comments"),
        _(
            "Is there anything else you would like to tell the larp coordinators?<br><br>Please mention here if the design of your larp requires a large number of your characters to be gendered (for example, a larp about a sauna night with the guys, or about female pilots in WWII).<br><br>When deciding which larps to include at Ropecon, we want as many larps as possible to be accessible for as many attendees as possible, regardless of their gender or the gender they prefer to larp as. Requiring a large number of your characters to be gendered may affect whether or not your submission for a larp is accepted.<br><br>You can also specify your preferred schedule here."
        ),
    ),
    is_in_english=(
        _("English OK"),
        _("If you are able, prepared and willing to run your larp in English if necessary, please tick this box."),
    ),
    is_age_restricted=(
        _("For players over 18 only"),
        _(
            "If your larp contains themes that require players to be 18 years or older, please tick this box. There will be an ID check for all players."
        ),
    ),
    ropecon2020_suitable_for_children_under_7=(
        _("Suitable for children under 7"),
        _(
            "If your larp is aimed at children under 7 years of age, please tick this box. You can also tick this box if your larp is suitable for children under 7 years, even if it is not specifically designed for them."
        ),
    ),
    ropecon2020_suitable_for_children_aged_7_12=(
        _("Suitable for children aged 7-12"),
        _(
            "If your larp is aimed at children 7-12 years of age, please tick this box. You can also tick this box if your larp is suitable for children aged 7-12 years, even if it is not specifically designed for them."
        ),
    ),
    ropecon2020_suitable_for_children_aged_12_plus=(
        _("Suitable for children aged 12+"),
        _(
            "If your larp is aimed at children over the age of 12, please tick this box. You can also tick this box if your larp is suitable for children aged 12 years and older, even if it is not specifically designed for them."
        ),
    ),
    ropecon2020_not_suitable_for_children=(
        _("Not suitable for children"),
        _("If your larp is not suitable for children under 15 years of age, please tick this box."),
    ),
    is_beginner_friendly=(
        _("Beginner-friendly"),
        _(
            "If your larp is suitable for players with very limited or without any previous experience about larping, please tick this box."
        ),
    ),
    ropecon2020_theme_end_of_the_world=(
        _("Theme: End of the world"),
        _("If your larp is related to the theme of Ropecon 2020 (end of the world), please tick this box."),
    ),
    ropecon2020_theme_dinosaurs=(
        _("Theme: Dinosaurs"),
        _("If your larp is related to the children’s theme of Ropecon 2020 (dinosaurs), please tick this box."),
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
            "approximate_length",
            "ropecon2018_sessions",
            "ropecon2018_characters",
            "min_players",
            "description",
            "content_warnings",
            "other_author",
            "ropecon2018_signuplist",
            "ropecon2018_space_requirements",
            "ropecon2018_prop_requirements",
            "ropecon2019_blocked_time_slots",
            "notes_from_host",
            Fieldset(
                _("Who is your larp for?"),
                "is_in_english",
                "is_age_restricted",
                "ropecon2020_suitable_for_children_under_7",
                "ropecon2020_suitable_for_children_aged_7_12",
                "ropecon2020_suitable_for_children_aged_12_plus",
                "ropecon2020_not_suitable_for_children",
                "is_beginner_friendly",
                "ropecon2020_theme_end_of_the_world",
                "ropecon2020_theme_dinosaurs",
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
        self.fields["ropecon2019_blocked_time_slots"].required = True

    class Meta:
        model = Programme
        fields = (
            "title",
            "approximate_length",
            "ropecon2018_sessions",
            "ropecon2018_characters",
            "min_players",
            "description",
            "content_warnings",
            "other_author",
            "ropecon2018_signuplist",
            "ropecon2018_space_requirements",
            "ropecon2018_prop_requirements",
            "ropecon2019_blocked_time_slots",
            "notes_from_host",
            "is_in_english",
            "is_age_restricted",
            "ropecon2020_suitable_for_children_under_7",
            "ropecon2020_suitable_for_children_aged_7_12",
            "ropecon2020_suitable_for_children_aged_12_plus",
            "ropecon2020_not_suitable_for_children",
            "is_beginner_friendly",
            "ropecon2020_theme_end_of_the_world",
            "ropecon2020_theme_dinosaurs",
        )

        widgets = dict(
            content_warnings=forms.Textarea,
            ropecon2019_blocked_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug="ropecon2020", slug="larp"),
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
    content_warnings=(
        _("Content warnings"),
        _("If your programme contains topics or themes that are heavy or distressing, please mention them here."),
    ),
    category=(
        _("Programme category"),
        _(
            "Choose the category that best suits your programme. Ropecon reserves the right to change the programme category if necessary."
        ),
    ),
    approximate_length=(
        _("Estimated duration (minutes)"),
        _(
            "Duration of presentations, panel discussions and other similar programme is either 45 minutes or 105 minutes. Duration of workshops is either 45 minutes, 105 minutes or 165 minutes. For other programme, please make an estimation."
        ),
    ),
    is_english_ok=(
        _("English OK"),
        _(
            "If you are able, prepared and willing to organise your programme in English if necessary, please tick this box."
        ),
    ),
    is_beginner_friendly=(
        _("Beginner-friendly"),
        _(
            "If your programme is suitable for people with very limited or without any previous knowledge about the subject, please tick this box."
        ),
    ),
    ropecon2020_suitable_for_children_under_7=(
        _("For children under 7"),
        _(
            "If your programme is aimed at children under 7 years of age, please tick this box. You can also tick this box if your programme is suitable for children under 7 years, even if it is not specifically aimed at them."
        ),
    ),
    ropecon2020_suitable_for_children_aged_7_12=(
        _("For children aged 7-12"),
        _(
            "If your programme is aimed at children 7-12 years of age, please tick this box. You can also tick this box if your programme is suitable for children aged 7-12 years, even if it is not specifically aimed at them."
        ),
    ),
    ropecon2020_suitable_for_children_aged_12_plus=(
        _("For children aged 12+"),
        _(
            "If your programme is aimed at children over the age of 12, please tick this box. You can also tick this box if your programme is suitable for children aged 12 years and older, even if it is not specifically aimed at them."
        ),
    ),
    ropecon2020_not_suitable_for_children=(
        _("Not suitable for children"),
        _("If your programme is not suitable for children under 15 years of age, please tick this box."),
    ),
    is_age_restricted=(
        _("For 18+ only"),
        _(
            "If your programme contains themes that require players to be 18 years or older, please tick this box. There will be an ID check for all participants."
        ),
    ),
    is_inaccessible=(
        _("Accessibility"),
        _(
            "If your programme contains any loud noises, flashing lights or other elements that can limit accessibility, please tick this box. More details can be provided in the Comments section below if necessary."
        ),
    ),
    ropecon2020_theme_end_of_the_world=(
        _("Theme: End of the world"),
        _("If your programme is related to the theme of Ropecon 2020 (end of the world), please tick this box."),
    ),
    ropecon2020_theme_dinosaurs=(
        _("Theme: Dinosaurs"),
        _("If your programme is related to the children’s theme of Ropecon 2020 (dinosaurs), please tick this box."),
    ),
    max_players=(
        _("Number of participants"),
        _(
            "If the number of participants in your workshop or other programme is limited, please provide the maximum number of participants."
        ),
    ),
    computer=(
        _("Laptop needs"),
        _(
            "What kind of a laptop will you use? We strongly recommend using a laptop provided by Ropecon. Using your own laptop is possible only when notified in advance."
        ),
    ),
    tech_requirements=(_("Other technical needs"), None),
    ropecon2019_blocked_time_slots=(
        _("When are you NOT able to host your programme?"),
        _(
            "Select the times when you DO NOT want to host your programme. Time slots have been intentionally left vague. If you have a more specific request in mind regarding your schedule, please let us know in the Comments section below."
        ),
    ),
    notes_from_host=(
        _("Comments"),
        _("Is there anything else you would like to tell the programme coordinators or organisers of Ropecon?"),
    ),
    is_available_for_panel=(
        _("Panel discussions"),
        _("I’m interested in participating in a panel discussion related to my field of expertise."),
    ),
    video_permission=(
        _("Recording & publishing consent"),
        _("Do you give Ropecon permission to record your programme and publish it on the Internet?"),
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
            "content_warnings",
            "category",
            "approximate_length",
            "is_english_ok",
            "is_beginner_friendly",
            "ropecon2020_suitable_for_children_under_7",
            "ropecon2020_suitable_for_children_aged_7_12",
            "ropecon2020_suitable_for_children_aged_12_plus",
            "ropecon2020_not_suitable_for_children",
            "is_age_restricted",
            "is_inaccessible",
            "ropecon2020_theme_end_of_the_world",
            "ropecon2020_theme_dinosaurs",
            "max_players",
            "computer",
            "tech_requirements",
            "ropecon2019_blocked_time_slots",
            "notes_from_host",
            "is_available_for_panel",
            "field_of_expertise",
            "video_permission",
        )

        for field_name, texts in PROGRAMME_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

        self.fields["description"].required = True
        self.fields["approximate_length"].required = True
        self.fields["video_permission"].required = True
        self.fields["approximate_length"].initial = 105

        self.fields["category"].queryset = Category.objects.filter(
            event=event,
            slug__in=(
                "pres",
                "panel",
                "disc",
                "craft",
                "mini",
                "music",
                "workshop",
                "dance",
                "other",
            ),
        )
        self.fields["computer"].choices = [
            ("con", _("Laptop provided by Ropecon")),
            ("pc", _("Own laptop (PC)")),
            ("mac", _("Own laptop (Mac)")),
            ("none", _("No laptop is needed in my programme")),
        ]
        self.fields["ropecon2019_blocked_time_slots"].required = True
        self.fields["video_permission"].choices = [
            ("public", _("I give permission to record and publish my programme")),
            ("forbidden", _("I do not give permission to record or publish my programme")),
        ]
        self.fields["video_permission"].blank = True

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "content_warnings",
            "category",
            "approximate_length",
            "is_english_ok",
            "is_beginner_friendly",
            "ropecon2020_suitable_for_children_under_7",
            "ropecon2020_suitable_for_children_aged_7_12",
            "ropecon2020_suitable_for_children_aged_12_plus",
            "ropecon2020_not_suitable_for_children",
            "is_age_restricted",
            "is_inaccessible",
            "ropecon2020_theme_end_of_the_world",
            "ropecon2020_theme_dinosaurs",
            "max_players",
            "computer",
            "tech_requirements",
            "ropecon2019_blocked_time_slots",
            "notes_from_host",
            "is_available_for_panel",
            "field_of_expertise",
            "video_permission",
        )

        widgets = dict(
            ropecon2019_blocked_time_slots=forms.CheckboxSelectMultiple,
        )


GAMING_DESK_FORM_FIELD_TEXTS = dict(
    category=(_("Game category"), _("Which category does your game programme belong to?")),
    ropecon2019_gaming_desk_subtype=(
        _("Game programme type"),
        _(
            "What type of game programme are you offering?<br><br>Tournament - organising your own game tournament or contest<br><br>Demonstration - showcasing, demonstrating and running demo games at the Experience Point<br><br>Open game - running games with or without specific scenarios by request<br><br>Other - Something other than mentioned above"
        ),
    ),
    title=(
        _("Game programme title"),
        _("Give your game programme a catchy and concise title. We reserve the right to edit the title if necessary."),
    ),
    approximate_length=(
        _("Estimated duration (minutes)"),
        _(
            "For 3 to 4 hours (180-240 minutes) of game programme you will receive a one-day ticket to Ropecon. For 6 to 8 hours (360-480 minutes) of game programme you will receive a weekend ticket to Ropecon."
        ),
    ),
    max_players=(_("Number of players"), _("How many players can participate in the game programme?")),
    description=(
        _("Description"),
        _(
            "Advertise your game for potential players. Inform players about what is expected of them, and what themes your game contains. If your game includes any heavy themes, such as physical violence or psychological abuse, please mention it here. Recommended length for descriptions is 300-500 characters. We reserve the right to edit and condense the description and the title if necessary."
        ),
    ),
    content_warnings=(
        _("Content warnings"),
        _(
            "If your game programme contains any heavy topics or themes that some players may find distressing, please mention them here."
        ),
    ),
    rpg_system=(
        _("Game system"),
        _(
            "What game system is used? For example, “Magic the Gathering”. If you designed the game system yourself, describe it in a few words. For example, “4X, space battle, conquest”"
        ),
    ),
    ropecon2018_signuplist=(
        _("Sign-up process"),
        _(
            "How will players sign up for your game programme?<br><br>No sign-up - No sign-up is required to participate.<br><br>Sign-up in advance - Please note that the sign-up for miniature wargame tournaments must open before 31st of May.<br><br>Sign-up at the Gaming Desk - Staff at the Gaming Desk will collect a list of participants. If signing up is required for your programme and it is not a miniature wargame tournament, choose this option."
        ),
    ),
    tech_requirements=(
        _("Space and technical needs"),
        _(
            "How much table space and how many chairs do you need for your game programme? Do you have any technical needs (for example, electricity)? Please keep in mind that we may not be able to fulfill all requests, so please justify how yours would benefit your game programme. Table size is 70 cm x 200 cm."
        ),
    ),
    ropecon2019_preferred_time_slots=(
        _("Preferred schedule"),
        _(
            "When would you like to host your game programme? Select the times when you ARE ABLE to host your game programme.<br><br>If you have a more specific request in mind regarding your schedule, please let us know in the Comments section below.<br><br>There are no restrictions on when you can or cannot host your game programme, but we reserve the right to make changes if necessary (for example, we would prefer to schedule tournaments to be held one after another rather than at the same time)."
        ),
    ),
    notes_from_host=(
        _("Comments"),
        _(
            "Is there anything else you would like to tell the organisers of Ropecon? You can also specify your preferred schedule here."
        ),
    ),
    is_in_english=(
        _("English OK"),
        _(
            "If you are able, prepared and willing to host your game programme in English if necessary, please tick this box."
        ),
    ),
    is_age_restricted=(
        _("For players over 18 only"),
        _(
            "If your game programme contains themes that require players to be 18 years or older, please tick this box. There will be an ID check for all players."
        ),
    ),
    ropecon2020_suitable_for_children_under_7=(
        _("Suitable for children under 7"),
        _(
            "If your game programme is aimed at children under 7 years of age, please tick this box. You can also tick this box if your game is suitable for children under 7 years, even if it is not specifically designed for them."
        ),
    ),
    ropecon2020_suitable_for_children_aged_7_12=(
        _("Suitable for children aged 7-12"),
        _(
            "If your game programme is aimed at children 7-12 years of age, please tick this box. You can also tick this box if your game is suitable for children aged 7-12 years, even if it is not specifically designed for them."
        ),
    ),
    ropecon2020_suitable_for_children_aged_12_plus=(
        _("Suitable for children aged 12+"),
        _(
            "If your game programme is aimed at children over the age of 12, please tick this box. You can also tick this box if your game is suitable for children aged 12 years and older, even if it is not specifically designed for them."
        ),
    ),
    ropecon2020_not_suitable_for_children=(
        _("Not suitable for children"),
        _("If your game programme is not suitable for children under 15 years of age, please tick this box."),
    ),
    is_beginner_friendly=(
        _("Beginner-friendly"),
        _(
            "If your game programme is suitable for players with very limited or without any previous knowledge about the game in question, please tick this box."
        ),
    ),
    ropecon2020_theme_end_of_the_world=(
        _("Theme: End of the world"),
        _("If your game programme is related to the theme of Ropecon 2020 (end of the world), please tick this box."),
    ),
    ropecon2020_theme_dinosaurs=(
        _("Theme: Dinosaurs"),
        _(
            "If your game programme is related to the children’s theme of Ropecon 2020 (dinosaurs), please tick this box."
        ),
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
            "category",
            "ropecon2019_gaming_desk_subtype",
            "title",
            "approximate_length",
            "max_players",
            "description",
            "content_warnings",
            "rpg_system",
            "ropecon2020_materials_language",
            "ropecon2018_signuplist",
            "tech_requirements",
            "ropecon2019_preferred_time_slots",
            "notes_from_host",
            Fieldset(
                _("Who is your game programme for?"),
                "is_in_english",
                "is_age_restricted",
                "ropecon2020_suitable_for_children_under_7",
                "ropecon2020_suitable_for_children_aged_7_12",
                "ropecon2020_suitable_for_children_aged_12_plus",
                "ropecon2020_not_suitable_for_children",
                "is_beginner_friendly",
                "ropecon2020_theme_end_of_the_world",
                "ropecon2020_theme_dinosaurs",
            ),
        )

        for field_name, texts in GAMING_DESK_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

        self.fields["category"].queryset = Category.objects.filter(
            event=event,
            slug__in=(
                "miniwar",
                "card",
                "board",
                "exp",
            ),
        )

        self.fields["ropecon2019_gaming_desk_subtype"].required = True
        self.fields["max_players"].initial = 3
        self.fields["max_players"].required = True
        self.fields["description"].required = True
        self.fields["ropecon2018_signuplist"].choices = [
            ("none", _("No sign-up")),
            ("itse", _("Sign-up in advance")),
            ("tiski", _("Sign-up at the Gaming Desk")),
        ]
        self.fields["ropecon2019_preferred_time_slots"].required = True

    class Meta:
        model = Programme
        fields = (
            "category",
            "ropecon2019_gaming_desk_subtype",
            "title",
            "approximate_length",
            "max_players",
            "description",
            "content_warnings",
            "rpg_system",
            "ropecon2020_materials_language",
            "ropecon2018_signuplist",
            "tech_requirements",
            "ropecon2019_preferred_time_slots",
            "notes_from_host",
            "is_in_english",
            "is_age_restricted",
            "ropecon2020_suitable_for_children_under_7",
            "ropecon2020_suitable_for_children_aged_7_12",
            "ropecon2020_suitable_for_children_aged_12_plus",
            "ropecon2020_not_suitable_for_children",
            "is_beginner_friendly",
            "ropecon2020_theme_end_of_the_world",
            "ropecon2020_theme_dinosaurs",
        )

        widgets = dict(
            content_warnings=forms.Textarea,
            ropecon2019_preferred_time_slots=forms.CheckboxSelectMultiple,
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
        self.fields["job_title"].required = True

    class Meta:
        model = Signup
        fields = ("job_title",)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(job_categories=JobCategory.objects.filter(event__slug="ropecon2020", name="Conitea"))


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
