# encoding: utf-8

from django import forms

from crispy_forms.layout import Layout, Fieldset

from core.forms import PersonForm
from core.models import Person
from core.utils import indented_without_label

from .models import Membership


class MemberForm(PersonForm):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            submit_button=False,
        )

        super(MemberForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            'first_name',
            'surname',
            'nick',
            'official_first_names',
            'muncipality',
            'birth_date',
            'phone',
            'email',
        )

        self.fields['muncipality'].help_text = u'Yhdistyslaki vaatii yhdistystä pitämään jäsenistään luetteloa, josta ilmenevät jäsenen täydellinen nimi ja kotikunta.'
        self.fields['phone'].help_text = None
        self.fields['email'].help_text = self.fields['email'].help_text.replace(u'tapahtumaan', u'yhdistykseen')

        for field_name, field in self.fields.iteritems():
            field.required = field_name in ['first_name', 'surname']

    class Meta:
        model = Person
        fields = [
            'first_name',
            'surname',
            'nick',
            'official_first_names',
            'muncipality',
            'birth_date',
            'phone',
            'email',
        ]


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('message',)
