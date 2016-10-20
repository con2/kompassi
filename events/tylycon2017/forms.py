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
            'shift_setup',
            'shift_cleanup',
            'total_work',
            # 'night_work',
            # indented_without_label('construction'),
            # indented_without_label('overseer'),

            indented_without_label('want_certificate'),
            # 'certificate_delivery_address',

            Fieldset(u'Lisätiedot',
                # 'shirt_size',
                'special_diet',
                'special_diet_other',
                # indented_without_label('need_lodging'),
                'prior_experience',
                'motivation',
                # 'shift_wishes',
                'free_text',
            )
        )


    class Meta:
        model = SignupExtra
        fields = (
            'shift_type',
            'shift_setup',
            'shift_cleanup',
            'total_work',
            # 'night_work',
            # 'construction',
            # 'overseer',
            'want_certificate',
            # 'certificate_delivery_address',
            # 'shirt_size',
            'special_diet',
            'special_diet_other',
            # 'need_lodging',
            'prior_experience',
            'motivation',
            # 'shift_wishes',
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
            Fieldset(u'Tehtävän tiedot',
                'job_title',
            ),
        )

        self.fields['job_title'].help_text = u"Mikä on tehtäväsi coniteassa? Printataan badgeen."
        self.fields['job_title'].required = True

    class Meta:
        model = Signup
        fields = ('job_title',)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            job_categories=JobCategory.objects.filter(event__slug='tylycon2017', name='Conitea')
        )


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super(OrganizerSignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Lisätiedot',
                # 'shirt_size',
                'special_diet',
                'special_diet_other',
            ),
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
            shift_type='kaikkikay',
            shift_setup=False,
            shift_cleanup=False,
            total_work='yli12h',
            # construction=False,
            # overseer=False,
            # need_lodging=False,
            want_certificate=False,
            # certificate_delivery_address=u'',
            prior_experience=u'',
            free_text=u'Syötetty käyttäen coniitin ilmoittautumislomaketta',
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
        )


class ProgrammeSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super(ProgrammeSignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'special_diet',
            'special_diet_other',
        )

    class Meta:
        model = SignupExtra
        fields = (
            'special_diet',
            'special_diet_other',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            work_days=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            shift_type='none',
            total_work='8h',
            free_text='Syötetty käyttäen ohjelmanjärjestäjän ilmoittautumislomaketta',
        )
