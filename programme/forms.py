# encoding: utf-8

from django import forms

from crispy_forms.layout import Layout, Fieldset

from core.models import Person
from core.utils import horizontal_form_helper, format_datetime

from .models import Programme, Role, Category, Room, AllRoomsPseudoView, START_TIME_LABEL


class ProgrammeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgrammeForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Ohjelmanumeron julkiset tiedot',
                'title',
                'description',
            ),
        )

    class Meta:
        model = Programme
        fields = (
            'title',
            'description',
        )


class ProgrammeExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'self_service' in kwargs:
            self_service = kwargs.pop('self_service')
        else:
            self_service = False

        super(ProgrammeExtraForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
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
            'room_requirements',
            'tech_requirements',
            'requested_time_slot',
            'video_permission',
            'notes_from_host',
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
        self.helper.form_tag = False
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
    # XXX
    start_time = forms.ChoiceField(choices=[], label=START_TIME_LABEL, required=False)

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammeAdminForm, self).__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(u'Ohjelmavastaavan merkinnät (eivät näy ohjelmanjärjestäjälle)',
                'category',
                'room',
                'start_time',
                'length',
                # 'tags',
                'notes',
            ),
        )

        self.fields['length'].widget.attrs['min'] = 0
        self.fields['category'].queryset = Category.objects.filter(event=event)
        self.fields['room'].queryset = Room.objects.filter(venue=event.venue)

        # XXX
        self.fields['start_time'].choices = [('', u'---------')] + [
            (
                start_time,
                format_datetime(start_time)
            ) for start_time in AllRoomsPseudoView(event).start_times()
        ]

    # XXX
    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time == '':
            start_time = None

        return start_time

    class Meta:
        model = Programme
        fields = (
            'category',
            'length',
            'notes',
            'room',
            'start_time',
        )

        widgets = dict(
            tags=forms.CheckboxSelectMultiple,
        )
