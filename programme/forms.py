from django import forms

from core.utils import horizontal_form_helper

from .models import Programme


class ProgrammeForm(models.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgrammeForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()

    class Meta:
        model = Programme
        fields = ('title', 'description', 'room_requirements', 'tech_requirements')