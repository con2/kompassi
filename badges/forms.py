# encoding: utf-8

from django import forms

from .models import Template

class CreateBadgeBatchForm(forms.Form):
    max_badges = forms.IntegerField(label=u"Kuinka monta badgea (enintään)?", initial=100)
    template = forms.ModelChoiceField(
        queryset=Template.objects.all(),
        required=False,
        label=u"Badgetyyppi",
        help_text=u"Jos jätät tämän kentän tyhjäksi, saat erän joka sisältää sekaisin eri badgetyyppejä.",
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(CreateBadgeBatchForm, self).__init__(*args, **kwargs)

        self.fields['template'].queryset = Template.objects.filter(event=event)

