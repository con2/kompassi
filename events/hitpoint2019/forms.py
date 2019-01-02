# encoding: utf-8



from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import Layout, Fieldset

from core.utils import horizontal_form_helper
from labour.forms import AlternativeFormMixin
from labour.models import Signup, JobCategory, WorkPeriod
from programme.models import AlternativeProgrammeFormMixin, Programme, Category

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'shift_type',
            'total_work',
            'night_work',
            'construction',
            'overseer',

            Fieldset('Työtodistus',
                'want_certificate',
                'certificate_delivery_address',
            ),
            Fieldset('Lisätiedot',
                'special_diet',
                'special_diet_other',
                'need_lodging',
                'prior_experience',
                'shift_wishes',
                'free_text',
            )
        )


    class Meta:
        model = SignupExtra
        fields = (
            'shift_type',
            'total_work',
            'night_work',
            'construction',
            'overseer',
            'want_certificate',
            'certificate_delivery_address',
            'special_diet',
            'special_diet_other',
            'need_lodging',
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


class OrganizerSignupForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        admin = kwargs.pop('admin')

        assert not admin

        super(OrganizerSignupForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Tehtävän tiedot',
                'job_title',
            ),
        )

        self.fields['job_title'].help_text = "Mikä on tehtäväsi coniteassa? Printataan badgeen."
        self.fields['job_title'].required = True

    class Meta:
        model = Signup
        fields = ('job_title',)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            job_categories=JobCategory.objects.filter(event__slug='hitpoint2019', name='Conitea')
        )


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super(OrganizerSignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Lisätiedot',
                'special_diet',
                'special_diet_other',
            ),
        )


    class Meta:
        model = SignupExtra
        fields = (
            'special_diet',
            'special_diet_other',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            shift_type='kaikkikay',
            total_work='yli12h',
            night_work='miel',
            construction=False,
            overseer=False,
            need_lodging=False,
            want_certificate=False,
            certificate_delivery_address='',
            prior_experience='',
            free_text='Syötetty käyttäen coniitin ilmoittautumislomaketta',
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
        )


DESCRIPTION_HELP_TEXT = _(
    'Advertise your game to potential players. Also explain, what is expected of players '
    'and what kind of themes are involved. Be extra sure to inform about potentially '
    'shocking themes. Recommended length is 300–500 characters. We reserve the right '
    'to edit this as necessary (including but not limited to shortening).'
)
APPROXIMATE_LENGTH_HELP_TEXT = _(
    'In order to gain free entry, you are required to run at in total least four '
    'hours of games.'
)


class RpgForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop('event')

        super(RpgForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'title',
            'rpg_system',
            'approximate_length',
            'min_players',
            'max_players',
            'description',
            'three_word_description',
            'hitpoint2017_preferred_time_slots',
            'notes_from_host',

            Fieldset(_('Whom is the game for?'),
                'is_english_ok',
                'is_children_friendly',
                'is_age_restricted',
                'is_beginner_friendly',
                'is_intended_for_experienced_participants',
            ),
        )

        self.fields['approximate_length'].help_text = APPROXIMATE_LENGTH_HELP_TEXT

        self.fields['three_word_description'].required = True
        self.fields['rpg_system'].required = True

        self.fields['description'].help_text = DESCRIPTION_HELP_TEXT
        self.fields['description'].required = True

    class Meta:
        model = Programme
        fields = (
            'title',
            'rpg_system',
            'approximate_length',
            'min_players',
            'max_players',
            'three_word_description',
            'description',
            'hitpoint2017_preferred_time_slots',
            'notes_from_host',
            'is_english_ok',
            'is_children_friendly',
            'is_age_restricted',
            'is_beginner_friendly',
            'is_intended_for_experienced_participants',
        )

        widgets = dict(
            hitpoint2017_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug='hitpoint2019', slug='roolipeli'),
        )


class FreeformForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    """
    If it is freeform
    But it is written on a form
    Then is it truly free of form?
    A questionable form of freedom
    """

    def __init__(self, *args, **kwargs):
        kwargs.pop('event')

        super(FreeformForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'title',
            'approximate_length',
            'min_players',
            'max_players',
            'description',
            'three_word_description',
            'physical_play',
            'other_author',

            'hitpoint2017_preferred_time_slots',
            'notes_from_host',

            Fieldset(_('Whom is the game for?'),
                'is_english_ok',
                'is_age_restricted',
                'is_beginner_friendly',
            ),
        )

        self.fields['approximate_length'].help_text = APPROXIMATE_LENGTH_HELP_TEXT

        self.fields['three_word_description'].required = True

        self.fields['description'].required = True
        self.fields['description'].help_text = DESCRIPTION_HELP_TEXT

    class Meta:
        model = Programme
        fields = (
            'title',
            'approximate_length',
            'min_players',
            'max_players',
            'description',
            'three_word_description',
            'physical_play',
            'other_author',

            'hitpoint2017_preferred_time_slots',
            'notes_from_host',

            'is_english_ok',
            'is_age_restricted',
            'is_beginner_friendly',

        )

        widgets = dict(
            hitpoint2017_preferred_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug='hitpoint2019', slug='freeform'),
        )
