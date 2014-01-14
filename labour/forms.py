# encoding: utf-8

from django import forms

from crispy_forms.layout import Layout, Fieldset

from core.models import Person
from core.utils import horizontal_form_helper

from .models import Signup, JobCategory, EmptySignupExtra


class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['job_categories'].queryset = JobCategory.objects.filter(event=self.instance.event, public=True)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Tehtävät',
                'job_categories'
            ),
        )

    class Meta:
        model = Signup
        fields = ('job_categories',)

        widgets = dict(
            job_categories=forms.CheckboxSelectMultiple
        )


class EmptySignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = EmptySignupExtra
        exclude = ('signup',)
