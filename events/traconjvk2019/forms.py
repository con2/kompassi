from django import forms

from core.utils import horizontal_form_helper
from enrollment.models import Enrollment


class EnrollmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()

        for field_name in (
            'personal_identification_number',
            'address',
            'zip_code',
            'city',
            'traconjv_expiring',
            'traconjv_when',
            'traconjv_solemnly_swear',
        ):
            self.fields[field_name].required = True

    class Meta:
        model = Enrollment
        fields = (
            'personal_identification_number',
            'address',
            'zip_code',
            'city',
            'traconjv_expiring',
            'traconjv_when',
            'traconjv_solemnly_swear',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            concon_parts=forms.CheckboxSelectMultiple,
        )
