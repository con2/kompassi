# encoding: utf-8

from django import forms

from crispy_forms.layout import Layout, Fieldset

from core.utils import horizontal_form_helper

from .models import SignupExtra

class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Lisätiedot',
                'shirt_size',
                'allergies',
                'prior_experience',
                'free_text'
            )
        )


    class Meta:
        model = SignupExtra
        fields = (
            'shirt_size',
            'allergies',
            'prior_experience',
            'free_text',
        )
