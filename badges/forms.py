# encoding: utf-8

from django import forms

from core.utils import horizontal_form_helper

from .models import Badge, Template

class CreateBatchForm(forms.Form):
    max_badges = forms.IntegerField(label=u"Kuinka monta badgea (enintään)?", initial=100)
    template = forms.ModelChoiceField(
        queryset=Template.objects.all(),
        required=False,
        label=u"Badgetyyppi",
        help_text=u"Jos jätät tämän kentän tyhjäksi, saat erän joka sisältää sekaisin eri badgetyyppejä.",
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(CreateBatchForm, self).__init__(*args, **kwargs)

        self.fields['template'].queryset = Template.objects.filter(event=event)


class BadgeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(BadgeForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
	self.helper.form_tag = False
        self.fields['template'].queryset = Template.objects.filter(event=event)

    class Meta:
        model = Badge
        fields = [
            'template',
            'job_title',
        ]


class HiddenBadgeCrouchingForm(forms.Form):
    badge_id = forms.IntegerField(required=True)
