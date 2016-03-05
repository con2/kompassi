# encoding: utf-8

from django import forms
from django.forms.models import modelformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from core.models import Person
from core.utils import (
    format_datetime,
    horizontal_form_helper,
    indented_without_label,
    make_horizontal_form_helper,
)

from .models import (
    AllRoomsPseudoView,
    Category,
    FreeformOrganizer,
    Invitation,
    Programme,
    ProgrammeRole,
    Role,
    Room,
    Tag,
)
from .models.programme import START_TIME_LABEL


class ProgrammePublicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammePublicForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['category'].queryset = Category.objects.filter(event=event)
        self.fields['tags'].queryset = Tag.objects.filter(event=event)

    class Meta:
        model = Programme
        fields = (
            'title',
            'description',
            'category',
            'tags',
        )

        widgets = dict(
            tags=forms.CheckboxSelectMultiple,
        )


class ProgrammeSelfServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammeSelfServiceForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        for field_name in [
            'title',
            'description',
        ]:
            self.fields[field_name].required = True

    class Meta:
        model = Programme
        fields = (
            'title',
            'description',
            'computer',
            'use_audio',
            'use_video',
            'number_of_microphones',
            'tech_requirements',
            'video_permission',
            'encumbered_content',
            'photography',
            'room_requirements',
            'requested_time_slot',
            'notes_from_host',
        )


class ProgrammeNeedsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammeNeedsForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Programme
        fields = (
            'computer',
            'use_audio',
            'use_video',
            'number_of_microphones',
            'tech_requirements',
            'video_permission',
            'encumbered_content',
            'photography',
            'room_requirements',
            'requested_time_slot',
            'notes_from_host',
        )


class ProgrammeInternalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammeInternalForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Programme
        fields = (
            'notes',
        )


class ScheduleForm(forms.ModelForm):
    start_time = forms.ChoiceField(choices=[], label=START_TIME_LABEL, required=False)

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ScheduleForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['length'].widget.attrs['min'] = 0
        self.fields['room'].queryset = Room.get_rooms_for_event(event)

        self.fields['start_time'].choices = [('', u'---------')] + [
            (
                start_time,
                format_datetime(start_time)
            ) for start_time in AllRoomsPseudoView(event).start_times()
        ]

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')

        if start_time == '':
            start_time = None

        return start_time

    class Meta:
        model = Programme
        fields = (
            'state',
            'room',
            'start_time',
            'length',
        )


class InvitationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(InvitationForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['role'].queryset = Role.objects.filter(personnel_class__event=event)

    class Meta:
        model = Invitation
        fields = (
            'email',
            'role',
        )


class FreeformOrganizerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FreeformOrganizerForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = FreeformOrganizer
        fields = (
            'text',
        )


class IdForm(forms.Form):
    id = forms.IntegerField()


class ChangeHostRoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ChangeHostRoleForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['role'].queryset = Role.objects.filter(personnel_class__event=event)

    class Meta:
        model = ProgrammeRole
        fields = (
            'role',
        )


class ChangeInvitationRoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ChangeInvitationRoleForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['role'].queryset = Role.objects.filter(personnel_class__event=event)

    class Meta:
        model = Invitation
        fields = (
            'role',
        )