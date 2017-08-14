from django import forms

from core.utils import horizontal_form_helper
from labour.forms import AlternativeFormMixin

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['work_days'].help_text = 'Minä päivinä olet halukas työskentelemään?'

    class Meta:
        model = SignupExtra
        fields = (
            'prior_experience',
            'shift_wishes',
            'free_text',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
            work_days=forms.CheckboxSelectMultiple,
        )


class ProgrammeSignupExtraForm(forms.ModelForm, AlternativeFormMixin):
    def __init__(self, *args, **kwargs):
        super(ProgrammeSignupExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = SignupExtra
        fields = ()

    def get_excluded_field_defaults(self):
        return dict(
            free_text='Syötetty käyttäen ohjelmanjärjestäjän ilmoittautumislomaketta',
        )
