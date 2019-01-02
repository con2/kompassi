from django import forms

from core.utils import horizontal_form_helper
from enrollment.models import Enrollment


class EnrollmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()

    class Meta:
        model = Enrollment
        fields = (
            'special_diet',
            'special_diet_other',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )
