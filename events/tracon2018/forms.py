from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import Layout, Fieldset

from core.utils import horizontal_form_helper, indented_without_label
from events.hitpoint2017.forms import APPROXIMATE_LENGTH_HELP_TEXT, DESCRIPTION_HELP_TEXT as RPG_DESCRIPTION_HELP_TEXT
from labour.forms import AlternativeFormMixin
from labour.models import Signup, JobCategory
from programme.models import Category, Programme, AlternativeProgrammeFormMixin

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'shift_type',
            'total_work',
            indented_without_label('overseer'),

            Fieldset('Työtodistus',
                indented_without_label('want_certificate'),
                'certificate_delivery_address',
            ),
            Fieldset('Lisätiedot',
                # 'shirt_size',
                'special_diet',
                'special_diet_other',
                'lodging_needs',
                'prior_experience',
                'shift_wishes',
                'free_text',
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            'shift_type',
            'total_work',
            'overseer',
            'want_certificate',
            'certificate_delivery_address',
            # 'shirt_size',
            'special_diet',
            'special_diet_other',
            'lodging_needs',
            'prior_experience',
            'shift_wishes',
            'free_text',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            lodging_needs=forms.CheckboxSelectMultiple,
        )

    def clean_certificate_delivery_address(self):
        want_certificate = self.cleaned_data['want_certificate']
        certificate_delivery_address = self.cleaned_data['certificate_delivery_address']

        if want_certificate and not certificate_delivery_address:
            raise forms.ValidationError(
                'Koska olet valinnut haluavasi työtodistuksen, on '
                'työtodistuksen toimitusosoite täytettävä.'
            )

        return certificate_delivery_address


class OrganizerSignupForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        kwargs.pop('event')
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
        # self.fields['job_title'].required = True

    class Meta:
        model = Signup
        fields = ('job_title',)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            job_categories=JobCategory.objects.filter(event__slug='tracon2018', name='Conitea')
        )


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super(OrganizerSignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Lisätiedot',
                # 'shirt_size',
                'special_diet',
                'special_diet_other',
                'email_alias',
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            # 'shirt_size',
            'special_diet',
            'special_diet_other',
            'email_alias',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            shift_type='kaikkikay',
            total_work='yli12h',
            overseer=False,
            want_certificate=False,
            certificate_delivery_address='',
            prior_experience='',
            free_text='Syötetty käyttäen coniitin ilmoittautumislomaketta',
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            lodging_needs=[],
        )


class ProgrammeSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super(ProgrammeSignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # 'shirt_size',
            'special_diet',
            'special_diet_other',
        )

    class Meta:
        model = SignupExtra
        fields = (
            # 'shirt_size',
            'special_diet',
            'special_diet_other',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            free_text='Syötetty käyttäen ohjelmanjärjestäjän ilmoittautumislomaketta',
            shift_type='kaikkikay',
            shirt_size='NO_SHIRT',
        )


class ProgrammeForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammeForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        for field_name in [
            'title',
            'description',
            'long_description',
            'length_from_host',
        ]:
            self.fields[field_name].required = True

        self.fields['category'].queryset = Category.objects.filter(event=event, public=True)

        self.fields['description'].help_text = (
            'Tämä kuvaus julkaistaan web-ohjelmakartassa sekä mahdollisessa ohjelmalehdessä. Kuvauksen '
            'tarkoitus on antaa osallistujalle riittävät tiedot päättää, osallistuako ohjelmaasi, sekä '
            'markkinoida ohjelmaasi. Pidä kuvaus kuitenkin ytimekkäänä, jotta se mahtuisi ohjelmalehteen. '
            'Ohjelmakuvauksen maksimipituus ohjelmalehteä varten on 720 merkkiä. Varaamme oikeuden muokata kuvausta.'
        )
        self.fields['description'].max_length = 720

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            'title',
            'description',
            'long_description',
            'length_from_host',
            'category',
            'computer',
            'use_audio',
            'use_video',
            'number_of_microphones',
            'tech_requirements',
            'video_permission',
            'encumbered_content',
            'photography',
            'rerun',
            'room_requirements',
            'requested_time_slot',
            'notes_from_host',
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

        self.fields['description'].help_text = RPG_DESCRIPTION_HELP_TEXT
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
            category=Category.objects.get(event__slug='tracon2018', slug='roolipeliohjelma'),
        )


class ShiftWishesSurvey(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop('event')

        super(ShiftWishesSurvey, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    @classmethod
    def get_instance_for_event_and_person(cls, event, person):
        return SignupExtra.objects.get(event=event, person=person)

    class Meta:
        model = SignupExtra
        fields = (
            'shift_wishes',
        )


class LodgingNeedsSurvey(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop('event')

        super(LodgingNeedsSurvey, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    @classmethod
    def get_instance_for_event_and_person(cls, event, person):
        return SignupExtra.objects.get(event=event, person=person)

    class Meta:
        model = SignupExtra
        fields = (
            'lodging_needs',
        )
        widgets = dict(
            lodging_needs=forms.CheckboxSelectMultiple,
        )
