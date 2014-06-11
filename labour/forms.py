# encoding: utf-8

from django import forms
from django.utils.timezone import now

from crispy_forms.layout import Layout, Fieldset

from core.forms import PersonForm
from core.models import Person
from core.utils import horizontal_form_helper, indented_without_label

from .models import Signup, JobCategory, EmptySignupExtra, ACCEPTED_STATES, TERMINAL_STATES

from datetime import date, datetime


# http://stackoverflow.com/a/9754466
def calculate_age(born, today):
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class AdminPersonForm(PersonForm):
    age_now = forms.IntegerField(required=False, label=u'Ikä nyt')
    age_event_start = forms.IntegerField(required=False, label=u'Ikä tapahtuman alkaessa')

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        super(AdminPersonForm, self).__init__(*args, **kwargs)

        self.fields['age_now'].initial = calculate_age(self.instance.birth_date, date.today())
        self.fields['age_now'].widget.attrs['readonly'] = True
        self.fields['age_event_start'].initial = calculate_age(self.instance.birth_date, event.start_time.date())
        self.fields['age_event_start'].widget.attrs['readonly'] = True

        # XXX copypasta
        self.helper.layout = Layout(
            'first_name',
            'surname',
            'nick',
            'preferred_name_display_style',
            'birth_date',
            'age_now', # not in PersonForm
            'age_event_start', # not in PersonForm
            'phone',
            'email',
            indented_without_label('may_send_info'),
        )


class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        job_categories = kwargs.pop('job_categories')
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['job_categories'].queryset = job_categories

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Tehtävät',
                'job_categories'
            ),
            Fieldset(u'Työvuorotoiveet',
                'work_periods'
            ),
        )

    def clean_job_categories(self):
        job_categories = self.cleaned_data['job_categories']

        if not all(jc.is_person_qualified(self.instance.person) for jc in job_categories):
            raise forms.ValidationError(u'Sinulla ei ole vaadittuja pätevyyksiä valitsemiisi tehtäviin.')

        return job_categories

    class Meta:
        model = Signup
        fields = ('job_categories', 'work_periods')

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple,
            work_periods=forms.CheckboxSelectMultiple,
        )


class EmptySignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = EmptySignupExtra
        exclude = ('signup',)


class SignupAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        job_categories = kwargs.pop('job_categories')
        super(SignupAdminForm, self).__init__(*args, **kwargs)
        self.fields['job_categories_accepted'].queryset = job_categories

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Signup
        fields = ('state', 'job_categories_accepted', 'notes')
        widgets = dict(
            job_categories_accepted=forms.CheckboxSelectMultiple,
        )

    def clean_job_categories_accepted(self):
        state = self.cleaned_data['state']
        job_categories_accepted = self.cleaned_data['job_categories_accepted']

        if state in ACCEPTED_STATES and not job_categories_accepted:
            raise forms.ValidationError(u'Kun ilmoittautuminen on hyväksytty, tulee valita vähintään yksi tehtäväalue.')
        elif state in TERMINAL_STATES and job_categories_accepted:
            raise forms.ValidationError(u'Kun ilmoittautuminen on hylätty, mikään tehtäväalue ei saa olla valittuna.')

        return job_categories_accepted
