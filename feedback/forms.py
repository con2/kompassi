
from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper

from .models import FeedbackMessage


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['feedback'].label = _('Your feedback')
        self.fields['feedback'].widget.attrs['required'] = 'required'

    class Meta:
        model = FeedbackMessage
        fields = ('feedback',)
