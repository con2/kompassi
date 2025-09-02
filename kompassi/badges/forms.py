from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import horizontal_form_helper
from kompassi.labour.models import PersonnelClass

from .models import Badge

MOON_RUNES_CHOICES = [
    ("dontcare", _("I don't care")),
    ("exclude", _("Exclude badges with moon runes")),
    ("onlyinclude", _("Only include badges with moon runes")),
]


class CreateBatchForm(forms.Form):
    max_items = forms.IntegerField(label="Kuinka monta badgea (enintään)?", initial=666, min_value=1, max_value=10000)
    personnel_class = forms.ModelChoiceField(
        queryset=PersonnelClass.objects.all(),
        required=False,
        label=_("Personnel class"),
        help_text=_("If you leave this field blank, you will receive a batch with mixed badge types."),
    )

    moon_rune_policy = forms.ChoiceField(
        choices=MOON_RUNES_CHOICES,
        label=_("Policy for badges with moon runes"),
        initial="dontcare",
        help_text=_(
            "Please state your policy towards badges with moon runes within this batch. "
            "You can choose to not care, to only include badges with moon runes, or to only include "
            "badges without moon runes. A badge with moon runes is defined as one whose contents cannot "
            'be encoded into ISO-8859-1. If unsure, select "I don\'t care".'
        ),
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.fields["personnel_class"].queryset = PersonnelClass.objects.filter(event=event)  # type: ignore


class BadgeForm(forms.ModelForm):
    formatted_perks = forms.CharField(
        label=_("Perks"),
        help_text=_("Will be shown in the onboarding view to instruct the onboarding desk what to give this person."),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.fields["personnel_class"].queryset = PersonnelClass.objects.filter(event=event)  # type: ignore

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data and not any(cleaned_data.get(key) for key in ("first_name", "surname", "nick")):
            raise ValidationError(_("At least one of first name, surname and nick must be provided."))

        return cleaned_data

    class Meta:
        model = Badge
        fields = [
            "personnel_class",
            "first_name",
            "surname",
            "nick",
            "job_title",
        ]


class HiddenBadgeCrouchingForm(forms.Form):
    badge_id = forms.IntegerField(required=True)
