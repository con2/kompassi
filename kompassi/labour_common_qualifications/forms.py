from django import forms

from kompassi.core.utils import DateField, horizontal_form_helper

from .models import JVKortti


class JVKorttiForm(forms.ModelForm):
    expiration_date = DateField(label="Viimeinen voimassaolopäivä")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = JVKortti
        fields = ("card_number", "expiration_date")
