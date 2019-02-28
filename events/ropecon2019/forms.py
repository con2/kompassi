from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import Layout, Fieldset

from core.forms import horizontal_form_helper
from programme.forms import AlternativeProgrammeFormMixin
from programme.models import Category, Programme

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'shift_type',

            Fieldset('Työtodistus',
                'want_certificate',
                'certificate_delivery_address',
            ),
            Fieldset('Lisätiedot',
                'special_diet',
                'special_diet_other',
                'prior_experience',
                'shift_wishes',
                'free_text',
            )
        )

    class Meta:
        model = SignupExtra
        fields = (
            'shift_type',
            'want_certificate',
            'certificate_delivery_address',
            'special_diet',
            'special_diet_other',
            'prior_experience',
            'shift_wishes',
            'free_text',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )

    def clean_certificate_delivery_address(self):
        want_certificate = self.cleaned_data['want_certificate']
        certificate_delivery_address = self.cleaned_data['certificate_delivery_address']

        if want_certificate and not certificate_delivery_address:
            raise forms.ValidationError('Koska olet valinnut haluavasi työtodistuksen, on '
                'työtodistuksen toimitusosoite täytettävä.')

        return certificate_delivery_address


class ProgrammeSignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = SignupExtra
        fields = (
            'special_diet',
            'special_diet_other',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )


RPG_FORM_FIELD_TEXTS = dict(
    title=(_('Game title'), None),
    rpg_system=(_('RPG system'), _('Which RPG system does the game use?')),
    approximate_length=(_('Game length (minutes)'), None),
    min_players=(_('Minimum number of players'), _('Pelaajien vähimmäismäärä')),
    max_players=(_('Maximum number of players'), None),
    is_in_english=(_('In English'), _('Please tick this box if the game is played in English.')),
    is_age_restricted=(_('Ages 18+ only'), _('Please tick this box if your game contains themes which require it to be restricted to players who are 18+ years old. Please give more details in the game description.')),
    is_children_friendly=(_('Suitable for children'), _('Please tick this box if your game is also suitable for children. If necessary, you can give more details in the game description.')),
    is_family_program=(_('Family program'), _('Please tick this box if your game has been designed also for the youngest players, and the players’ guardians may help the players or participate in the game with them. If necessary, you can give more details in the game description.')),
    is_intended_for_experienced_participants=(_('For experienced players'), _('Check this if the game requires knowledge of the world or the rules of the game.')),
    description=(_('Description'), _('Advertise your game to potential players. Be extra sure to inform about potentially shocking or disturbing themes. Recommended length is 300–500 characters. We reserve the right to edit the text as necessary.<br><br>Please write the description at least in the language the game will be run in (English or Finnish). You may include the description in both languages, if you wish.')),
    three_word_description=(_('Short blurb'), _('Summarize your game in one sentence which helps potential players get the gist of your game. For example, “Traditional D&D dungeon adventure” or “Lovecraftian horror in Equestria”. We reserve the right to edit the text.')),
    notes_from_host=(_('Other information for the RPG coordinator'), _('If there is anything else you wish to say to the RPG coordinator that is not covered by the above questions, please enter it here.')),
)


class RpgForm(AlternativeProgrammeFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        admin = kwargs.pop('admin') if 'admin' in kwargs else False

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'title',
            'rpg_system',
            'approximate_length',
            'min_players',
            'max_players',
            'is_revolving_door',
            Fieldset(_('Who is the game meant for?'),
                'is_in_english',
                'is_age_restricted',
                'is_children_friendly',
                'is_family_program',
                'is_beginner_friendly',
                'is_intended_for_experienced_participants',
            ),
            Fieldset(_('Game genre (Choose all which apply)'),
                'ropecon2018_genre_fantasy',
                'ropecon2018_genre_scifi',
                'ropecon2018_genre_historical',
                'ropecon2018_genre_modern',
                'ropecon2018_genre_war',
                'ropecon2018_genre_horror',
                'ropecon2019_genre_adventure',
                'ropecon2018_genre_mystery',
                'ropecon2018_genre_drama',
                'ropecon2018_genre_humor',
            ),
            Fieldset(_('Game style (Choose any which apply)'),
                'ropecon2018_style_serious',
                'ropecon2018_style_light',
                'ropecon2018_style_rules_heavy',
                'ropecon2018_style_rules_light',
                'ropecon2018_style_story_driven',
                'ropecon2018_style_character_driven',
                'ropecon2018_style_combat_driven',
                'description',
                'three_word_description',
                'ropecon2019_blocked_time_slots',
                'notes_from_host',
            )
        )

        for field_name, texts in RPG_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

    class Meta:
        model = Programme
        fields = [
            'title',
            'rpg_system',
            'approximate_length',
            'min_players',
            'max_players',
            'is_revolving_door',

            # Who is the game meant for?
            'is_in_english',
            'is_age_restricted',
            'is_children_friendly',
            'is_family_program',
            'is_beginner_friendly',
            'is_intended_for_experienced_participants',

            # Genre
            'ropecon2018_genre_fantasy',
            'ropecon2018_genre_scifi',
            'ropecon2018_genre_historical',
            'ropecon2018_genre_modern',
            'ropecon2018_genre_war',
            'ropecon2018_genre_horror',
            'ropecon2019_genre_adventure',
            'ropecon2018_genre_mystery',
            'ropecon2018_genre_drama',
            'ropecon2018_genre_humor',

            # Style
            'ropecon2018_style_serious',
            'ropecon2018_style_light',
            'ropecon2018_style_rules_heavy',
            'ropecon2018_style_rules_light',
            'ropecon2018_style_story_driven',
            'ropecon2018_style_character_driven',
            'ropecon2018_style_combat_driven',

            'description',
            'three_word_description',
            'ropecon2019_blocked_time_slots',
            'notes_from_host',
        ]

        widgets = dict(
            ropecon2019_blocked_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug='ropecon2019', slug='rpg'),
        )


LARP_FORM_FIELD_TEXTS = dict(
    title=(_('Title of the larp'), _('Come up with a catchy and concise name for your larp. Ropecon reserves the right to edit the title.')),
    approximate_length=(_('Estimated duration (minutes)'), _('For one run of a 3-4 hour game (180-240 minutes) of your own writing you will receive one free weekend ticket. This includes time for propping, brief and debrief, as well as the actual game time.')),
    ropecon2018_sessions=(_('Number of runs'), _('Here you can request how many times you would like to run your game during the convention. Due to limited space we may not be able to fulfill all requests.<br><br>For one run of a 3-4 hour game of your own writing or two runs of a pre-written scenario you will receive one free weekend ticket. Additional runs of your game will yield an extra one-day ticket.')),
    notes_from_host=(_('Comments'), _('Is there anything else you would like to tell the organizers?<br><br>Please mention here if the design of your game dictates that some of the characters need to be a specific gender (eg. larps about a men’s sauna night or World War II female fighter pilots).<br><br>We would like the larp program as a whole to offer something for all attendees, even if not all players wish to play all genders. Due to this, some larps may be cut from the program.<br><br>You can also enter your more specific scheduling preferences here.')),
    is_english_ok=(_('The game can be run in English'), _('If you are able, prepared and willing to organise your program in English if necessary, please tick this box.')),
    is_age_restricted=(_('The game is intended for players over 18'), _('Please tick this box if your game involves themes necessitating that all players are 18 years or older.')),
    is_children_friendly=(_('The game is intended for children'), _('Please tick this box if your game is designed for children.')),
    is_beginner_friendly=(_('Beginner-friendly'), _('If your game is suitable for players without any or with very limited larping experience, please tick this box.')),
    is_family_program=(_('Family-friendly'), None),
)


class LarpForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop('event')
        admin = kwargs.pop('admin') if 'admin' in kwargs else False

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'title',
            'approximate_length',
            'ropecon2018_sessions',
            'ropecon2018_characters',
            'min_players',
            'description',
            'content_warnings',
            'other_author',
            'ropecon2018_signuplist',
            'ropecon2018_space_requirements',
            'ropecon2018_prop_requirements',
            'ropecon2019_blocked_time_slots',
            'notes_from_host',

            Fieldset(_('Whom is the game for?'),
                'is_english_ok',
                'is_age_restricted',
                'is_children_friendly',
                'is_beginner_friendly',
                'is_family_program',
            ),
        )

        for field_name, texts in LARP_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

        self.fields['ropecon2018_sessions'].initial = 2
        self.fields['ropecon2018_characters'].initial = 10

    class Meta:
        model = Programme
        fields = (
            'title',
            'approximate_length',
            'ropecon2018_sessions',
            'ropecon2018_characters',
            'min_players',
            'description',
            'content_warnings',
            'other_author',
            'ropecon2018_signuplist',
            'ropecon2018_space_requirements',
            'ropecon2018_prop_requirements',
            'ropecon2019_blocked_time_slots',
            'notes_from_host',

            'is_english_ok',
            'is_age_restricted',
            'is_children_friendly',
            'is_beginner_friendly',
            'is_family_program',
        )

        widgets = dict(
            ropecon2019_blocked_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug='ropecon2018', slug='larp'),
        )



PROGRAMME_FORM_FIELD_TEXTS = dict(
    title=(_('Title'), _('Come up with a catchy, concise title for your program. Ropecon reserves the right to edit the title if necessary.')),
    description=(_('Description'), _('Describe your program to your potential audience or participants in an appealing way. If your program contains topics that are heavy or potentially distressing, please pay special attention to this in the description. Recommended length is 300-500 characters. Ropecon reserves the right to edit the description and title of the program if necessary, for example reducing their length.')),
    category=(_('Program category'), _('Choose the program category that best suits your program. Ropecon reserves the right to change the program category if necessary.')),
    approximate_length=(_('Estimated duration (minutes)'), _('Duration of lectures and panel discussions is either 45 minutes or 105 minutes. Duration of workshops is either 45 minutes, 105 minutes or 165 minutes. For other program, please make an estimation.')),
    is_family_program=(_('Family-friendly'), _('If your program is suitable for or aimed at children, teenagers or families, please tick the checkbox. More details can be provided in the last text field.')),
    max_players=(_('Max. number of participants'), _('If your workshop or other program can only host a limited number of participants, please provide a maximum number of attendees.')),
    ropecon2019_blocked_time_slots=(_('Preferred schedule'), _('Select the times when you DO NOT want to have your program. Time slots have been intentionally left vague. If you have further requests on time slots and schedule, more details can be provided in the open comment field below.')),
    notes_from_host=(_('Comments'), _('Do you have any further information, details, comments or questions that you would like to let our program coordinators to know?')),
)


class ProgrammeForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        admin = kwargs.pop('admin') if 'admin' in kwargs else False

        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'title',
            'description',
            'content_warnings',
            'category',
            'approximate_length',
            'is_english_ok',
            'is_children_friendly',
            'is_beginner_friendly',
            'is_inaccessible',
            'is_family_program',
            'is_age_restricted',
            'max_players',
            'computer',
            'tech_requirements',
            'ropecon2019_blocked_time_slots',
            'notes_from_host',
            'is_available_for_panel',
            'video_permission',
        )

        for field_name, texts in PROGRAMME_FORM_FIELD_TEXTS.items():
            self.fields[field_name].label, self.fields[field_name].help_text = texts

        self.fields['category'].queryset = Category.objects.filter(event=event, slug__in=(
            'pres',
            'panel',
            'disc',
            'craft',
            'mini',
            'music',
            'workshop',
            'other',
        ))

    class Meta:
        model = Programme
        fields = (
            'title',
            'description',
            'content_warnings',
            'category',
            'approximate_length',
            'is_english_ok',
            'is_children_friendly',
            'is_beginner_friendly',
            'is_inaccessible',
            'is_family_program',
            'is_age_restricted',
            'max_players',
            'computer',
            'tech_requirements',
            'ropecon2019_blocked_time_slots',
            'notes_from_host',
            'is_available_for_panel',
            'video_permission',
        )

        widgets = dict(
            ropecon2019_blocked_time_slots=forms.CheckboxSelectMultiple,
        )
