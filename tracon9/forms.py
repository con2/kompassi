# encoding: utf-8

from django import forms

from crispy_forms.layout import Layout, Fieldset

from core.utils import horizontal_form_helper, indented_without_label

from .models import SignupExtra

class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Työtodistus',
                indented_without_label('want_certificate'),
                'certificate_delivery_address',
            ),
            Fieldset(u'Lisätiedot',
                'shirt_size',
                'allergies',
                'prior_experience',
                'free_text',
            )
        )


    class Meta:
        model = SignupExtra
        fields = (
            'want_certificate',
            'certificate_delivery_address',
            'shirt_size',
            'allergies',
            'prior_experience',
            'free_text',
        )


    def clean_certificate_delivery_address(self):
        want_certificate = self.cleaned_data['want_certificate']
        certificate_delivery_address = self.cleaned_data['certificate_delivery_address']

        if want_certificate and not certificate_delivery_address:
            raise forms.ValidationError(u'Koska olet valinnut haluavasi työtodistuksen, on '
                u'työtodistuksen toimitusosoite täytettävä.')

        return certificate_delivery_address
