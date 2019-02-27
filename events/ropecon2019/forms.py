from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import Layout, Fieldset

from core.forms import horizontal_form_helper
from programme.forms import AlternativeProgrammeFormMixin
from programme.models import Programme

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
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
                'notes_from_host',
            )
        )

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
        ]

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug='ropecon2019', slug='roolipeli'),
        )
