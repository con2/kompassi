from crispy_forms.helper import FormHelper
from django import forms
from django.utils.translation import gettext_lazy as _


class FeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea, label=_("Your feedback"), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
