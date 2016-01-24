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
    Category,
    Invitation,
    Programme,
    Role,
    Room,
    Tag,
)


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


class ProgrammeNeedsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammeNeedsForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Programme
        fields = (
            'room_requirements',
            'tech_requirements',
            'requested_time_slot',
            'notes_from_host',
            'video_permission',
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
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ScheduleForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['room'].queryset = Room.objects.filter(venue=event.venue)
        # XXX start_time.queryset

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
        super(InvitationForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Invitation
        fields = (
            'email',
            'role',
        )
