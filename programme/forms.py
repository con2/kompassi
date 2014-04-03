# encoding: utf-8

from django import forms

from crispy_forms.layout import Layout, Fieldset

from core.models import Person
from core.utils import horizontal_form_helper

from .models import Programme, Role


class ProgrammeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'self_service' in kwargs:
            self_service = kwargs.pop('self_service')
        else:
            self_service = False

        super(ProgrammeForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            Fieldset(u'Ohjelmanumeron julkiset tiedot',
                'title',
                'description',
            ),
            Fieldset(u'Järjestäjien tarvitsemat lisätiedot',
                'room_requirements',
                'tech_requirements',
                'requested_time_slot',
                'video_permission',
                'notes_from_host',
            ),
        )

        if self_service:
            for field_name in [
                'room_requirements',
                'tech_requirements',
                'requested_time_slot',
            ]:
                self.fields[field_name].required = True

    class Meta:
        model = Programme
        fields = (
            'description',
            'notes_from_host',
            'requested_time_slot',
            'room_requirements',
            'tech_requirements',
            'title',
            'video_permission',
        )


class ProgrammePersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'self_service' in kwargs:
            self_service = kwargs.pop('self_service')
        else:
            self_service = False

        super(ProgrammePersonForm, self).__init__(*args, **kwargs)

        if self_service:
            for field_name in [
                'email',
                'phone'
            ]:
                self.fields[field_name].required = True

        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            'first_name',
            'surname',
            'nick',
            'preferred_name_display_style',
            'phone',
            'email',
            indented_without_label('may_send_info'),
        )

    class Meta:
        model = Person
        fields = [
            'email',
            'first_name',
            'may_send_info',
            'nick',
            'phone',
            'preferred_name_display_style',
            'surname',
        ]


class ProgrammeAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgrammeAdminForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.layout = Layout(
            Fieldset(u'Ohjelmavastaavan merkinnät (eivät näy ohjelmanjärjestäjälle)',
                'category',
                'room',
                'start_time',
                'length',
                'tags',
                'notes',
            ),
        )

        self.fields['length'].widget.attrs['min'] = 0

    class Meta:
        model = Programme
        fields = (
            'category',
            'length',
            'notes',
            'room',
            'start_time',
            'tags',
        )

        widgets = dict(
            tags=forms.CheckboxSelectMultiple,
        )
