from django import forms
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import horizontal_form_helper

from .models import EnrollmentEventMeta


class EnrollmentStartForm(forms.ModelForm):
    """
    Used in the /events/xxxx/enrollment/admin/start view to show fields for
    starting and ending times for the enrollment period.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    def clean_registration_closes(self):
        enrollment_opens = self.cleaned_data.get("enrollment_opens")
        enrollment_closes = self.cleaned_data.get("enrollment_closes")

        if enrollment_opens and enrollment_closes and enrollment_opens >= enrollment_closes:
            raise forms.ValidationError(_("The closing time must be after the opening time."))

        return enrollment_closes

    class Meta:
        model = EnrollmentEventMeta
        fields = (
            "enrollment_opens",
            "enrollment_closes",
        )
