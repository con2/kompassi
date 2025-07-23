import re

from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import horizontal_form_helper

from ..models import ProgrammeFeedback


class ProgrammeFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        is_own_programme = kwargs.pop("is_own_programme")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        if is_own_programme:
            self.fields["is_anonymous"].disabled = True
            self.fields["is_anonymous"].help_text = _(
                "Because you are the host of this programme, you cannot leave " "your feedback anonymously."
            )

    class Meta:
        model = ProgrammeFeedback
        fields = (
            "feedback",
            "is_anonymous",
        )


kissa_validator = RegexValidator(
    regex=r"^kissa$",
    flags=re.IGNORECASE,
    message="Vihje: kissa",
)


class AnonymousProgrammeFeedbackForm(forms.ModelForm):
    kissa = forms.CharField(
        label="Mikä eläin sanoo miau?",
        help_text="Tällä tarkistamme, että et ole robotti.",
        validators=[
            kissa_validator,
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = ProgrammeFeedback
        fields = ("feedback",)
