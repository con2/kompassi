# encoding: utf-8

from __future__ import unicode_literals

from django import forms
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from core.models import Person
from core.utils import (
    format_datetime,
    horizontal_form_helper,
    indented_without_label,
    make_horizontal_form_helper,
    initialize_form_set,
)

from .models import (
    AllRoomsPseudoView,
    Category,
    FreeformOrganizer,
    Invitation,
    Programme,
    ProgrammeEventMeta,
    ProgrammeFeedback,
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

        self.fields['start_time'].choices = [('', '---------')] + [
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
            'frozen',
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
            'extra_invites',
        )


class SiredInvitationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SiredInvitationForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['email'].widget.attrs['placeholder'] = _('Please enter an e-mail address to invite another host')
        self.fields['email'].label = False

    class Meta:
        model = Invitation
        fields = (
            'email',
        )


def get_sired_invitation_formset(request, invitation_or_programme_role):
    SiredInvitationFormset = modelformset_factory(Invitation,
        form=SiredInvitationForm,
        validate_max=True,
        extra=invitation_or_programme_role.extra_invites_left,
        max_num=invitation_or_programme_role.extra_invites_left,
    )

    return initialize_form_set(SiredInvitationFormset, request,
        queryset=Invitation.objects.none(),
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
            'extra_invites',
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
            'extra_invites',
        )


class PublishForm(forms.ModelForm):
    # XXX get a date picker
    public_from = forms.DateTimeField(
        required=False,
        label=_("Public from"),
    )
    # public_until = forms.DateTimeField(
    #     required=False,
    #     label=_("Public until"),
    #     help_text=_("Format: YYYY-MM-DD HH:MM:SS"),
    # )

    def __init__(self, *args, **kwargs):
        super(PublishForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    # def clean_registration_closes(self):
    #     registration_opens = self.cleaned_data.get('registration_opens')
    #     registration_closes = self.cleaned_data.get('registration_closes')

    #     if registration_opens and registration_closes and registration_opens >= registration_closes:
    #         raise forms.ValidationError(_("The registration closing time must be after the registration opening time."))

    #     return registration_closes

    class Meta:
        model = ProgrammeEventMeta
        fields = (
            'public_from',
        )


class ProgrammeFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgrammeFeedbackForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = ProgrammeFeedback
        fields = (
            'feedback',
            'is_anonymous',
        )
