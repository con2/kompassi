# encoding: utf-8

from __future__ import unicode_literals

from django import forms

from crispy_forms.layout import Layout, Fieldset

from core.utils import horizontal_form_helper, indented_without_label
from labour.forms import AlternativeFormMixin
from labour.models import Signup, JobCategory, WorkPeriod

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Erikoisruokavalio',
                'special_diet',
                'special_diet_other',
            ),
            Fieldset('Työvuorotoiveet',
                'total_work',
                'shift_type',
                'working_days',
                'shift_wishes',
            ),
            Fieldset('Lisätiedot',
                'prior_experience',
                'free_text',
            ),
        )


    class Meta:
        model = SignupExtra
        fields = (
            'special_diet',
            'special_diet_other',
            'total_work',
            'shift_type',
            'working_days',
            'shift_wishes',
            'prior_experience',
            'free_text',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )


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

        self.fields['job_title'].help_text = 'Mikä on tehtäväsi vastaavassa? Printataan badgeen.'
        # self.fields['job_title'].required = True

    class Meta:
        model = Signup
        fields = (
            'job_title',
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            job_categories=JobCategory.objects.filter(event__slug='shippocon2016', name='Vastaava')
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
            shift_type='yksipitka',
            total_work='12h',
            working_days='pela',
            prior_experience='',
            free_text='Syötetty käyttäen vastaavan ilmoittautumislomaketta',
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            lodging_needs=[],
        )
