# encoding: utf-8

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
            'shift_type',
            'shirt_size',

            Fieldset(
                u'Lisätiedot',
                'desu_amount',
                indented_without_label('night_work'),
                'prior_experience',
                'free_text',
            )
        )

    class Meta:
        model = SignupExtra
        fields = (
            'shift_type',
            'shirt_size',
            'desu_amount',
            'night_work',
            'prior_experience',
            'free_text',
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
            Fieldset(u'Tehtävän tiedot',
                'job_title',
            ),
        )

        self.fields['job_title'].help_text = u"Mikä on tehtäväsi vastaavana? Printataan badgeen."
        # self.fields['job_title'].required = True

    class Meta:
        model = Signup
        fields = ('job_title',)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            work_periods=WorkPeriod.objects.filter(event__slug='frostbite2016'),
            job_categories=JobCategory.objects.filter(event__slug='frostbite2016', name='Vastaava')
        )


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super(OrganizerSignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                u'Lisätiedot',
                'shirt_size',
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            'shirt_size',
        )

    def get_excluded_field_defaults(self):
        return dict(
            free_text=u'Syötetty käyttäen vastaavan ilmoittautumislomaketta',
        )
