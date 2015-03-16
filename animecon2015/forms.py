# encoding: utf-8

from django import forms
from localflavor.fi.forms import FISocialSecurityNumber

from crispy_forms.layout import Layout, Fieldset

from core.utils import horizontal_form_helper, indented_without_label
from labour.forms import AlternativeFormMixin
from labour.models import Signup, JobCategory, WorkPeriod

from .models import SignupExtra, KORTITON_JV_HETU_LABEL, KORTITON_JV_HETU_HELP_TEXT


class SignupExtraForm(forms.ModelForm):
    personal_identification_number = FISocialSecurityNumber(
        required=False,
        label=KORTITON_JV_HETU_LABEL,
        help_text=KORTITON_JV_HETU_HELP_TEXT,
    )

    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'total_work',
            Fieldset(u'Kortittomien järjestyksenvalvojien lisätiedot',
                'personal_identification_number',
            ),
            Fieldset(u'Työtodistus',
                indented_without_label('want_certificate'),
                'certificate_delivery_address',
            ),
            Fieldset(u'Lisätiedot',
                'special_diet',
                'special_diet_other',
                'lodging_needs',
                'prior_experience',
                'free_text',
            )
        )


    class Meta:
        model = SignupExtra
        fields = (
            'total_work',
            'personal_identification_number',
            'want_certificate',
            'certificate_delivery_address',
            'special_diet',
            'special_diet_other',
            'lodging_needs',
            'prior_experience',
            'free_text',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            lodging_needs=forms.CheckboxSelectMultiple,
        )

    def clean_personal_identification_number(self):
        personal_identification_number = self.cleaned_data['personal_identification_number']
        kortiton_jv = JobCategory.objects.get(
            event__slug='animecon2015',
            name=u'Kortiton järjestyksenvalvoja',
        )

        # XXX HORRIBLE HACK job_categories is in signupform, this is signupextraform
        # Cannot use self.instance.signup.job_categories because it is not necessarily saved yet.
        if unicode(kortiton_jv.pk) in self.data.getlist('signup-job_categories', []):
            if not personal_identification_number:
                raise forms.ValidationError(u'Koska haet kortittomaksi järjestyksenvalvojaksi, on henkilötunnus annettava.')
        elif personal_identification_number:
            raise forms.ValidationError(u'Koska et hae kortittomaksi järjestyksenvalvojaksi, tulee henkilötunnuskenttä jättää tyhjäksi.')

        return personal_identification_number

    def clean_certificate_delivery_address(self):
        want_certificate = self.cleaned_data['want_certificate']
        certificate_delivery_address = self.cleaned_data['certificate_delivery_address']

        if want_certificate and not certificate_delivery_address:
            raise forms.ValidationError(u'Koska olet valinnut haluavasi työtodistuksen, on '
                u'työtodistuksen toimitusosoite täytettävä.')

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
            Fieldset(u'Tehtävän tiedot',
                'job_title',
            ),
        )

        self.fields['job_title'].help_text = u"Mikä on tehtäväsi coniteassa? Printataan badgeen."
        # self.fields['job_title'].required = True

    class Meta:
        model = Signup
        fields = ('job_title',)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            work_periods=WorkPeriod.objects.filter(event__slug='traconx'),
            job_categories=JobCategory.objects.filter(event__slug='traconx', name='Conitea')
        )


class OrganizerSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super(OrganizerSignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Lisätiedot',
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
            total_work='ekstra',
            want_certificate=False,
            certificate_delivery_address=u'',
            prior_experience=u'',
            free_text=u'Syötetty käyttäen coniitin ilmoittautumislomaketta',
        )

    def get_excluded_m2m_field_defaults(self):
        return dict(
            lodging_needs=[],
        )
