# encoding: utf-8

from django import forms

from crispy_forms.layout import Layout, Fieldset

from core.forms import PersonForm
from core.models import Person
from core.utils import indented_without_label, horizontal_form_helper

from .models import Membership


class MemberForm(PersonForm):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            submit_button=False,
        )

        super(MemberForm, self).__init__(*args, **kwargs)

        self.helper.form_tag = False
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


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('message',)


class MembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MembershipForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            'state',
            'message',
        )

    class Meta:
        model = Membership
        fields = ('state', 'message',)