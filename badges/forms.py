# encoding: utf-8

from django import forms
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from core.utils import horizontal_form_helper
from labour.models import PersonnelClass

from .models import Badge


class CreateBatchForm(forms.Form):
    max_items = forms.IntegerField(label=u"Kuinka monta badgea (enintään)?", initial=100)
    personnel_class = forms.ModelChoiceField(
        queryset=PersonnelClass.objects.all(),
        required=False,
        label=_(u"Personnel class"),
        help_text=_(u"If you leave this field blank, you will receive a batch with mixed badge types."),
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(CreateBatchForm, self).__init__(*args, **kwargs)

        self.fields['personnel_class'].queryset = PersonnelClass.objects.filter(event=event)


class BadgeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(BadgeForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.fields['personnel_class'].queryset = PersonnelClass.objects.filter(event=event)

    def clean(self):
        cleaned_data = super(BadgeForm, self).clean()

        if not any(cleaned_data.get(key) for key in ('first_name', 'surname', 'nick')):
            raise ValidationError(_(u'At least one of first name, surname and nick must be provided.'))

        return cleaned_data

    class Meta:
        model = Badge
        fields = [
            'personnel_class',
            'first_name',
            'surname',
            'nick',
            'job_title',
        ]


class HiddenBadgeCrouchingForm(forms.Form):
    badge_id = forms.IntegerField(required=True)
