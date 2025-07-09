from crispy_forms.layout import Fieldset, Layout
from django import forms

from core.utils import horizontal_form_helper

from .models import SignupExtra


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # "shift_type",
            # indented_without_label("night_work"),
            Fieldset(
                "Lisätiedot",
                # indented_without_label("need_lodging"),
                # indented_without_label("want_certificate"),
                # "shirt_size",
                "special_diet",
                "special_diet_other",
                "skills",
                "experience",
                "free_text",
            ),
        )

    class Meta:
        model = SignupExtra
        fields = (
            # "shift_type",
            # "shirt_size",
            "special_diet",
            "special_diet_other",
            # "night_work",
            # "want_certificate",
            "skills",
            "experience",
            "free_text",
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )
