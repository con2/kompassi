# encoding: utf-8

from __future__ import unicode_literals

from django import forms
from django.db.models import Q
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
    AlternativeProgrammeForm,
    AlternativeProgrammeFormMixin,
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
from .proxies.programme_event_meta.cold_offers import ColdOffersProgrammeEventMetaProxy
from .models.programme import START_TIME_LABEL


class ProgrammeAdminCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammeAdminCreateForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields['form_used'].queryset = AlternativeProgrammeForm.objects.filter(event=event)
        self.fields['form_used'].help_text = _(
            'Select the form that will be used to edit the information of this programme. '
            'If this field is left blank, the default form will be used. '
            'Some events do not offer a choice of different forms, in which case '
            'this field will not have options and the default form will always be used. '
        )

        self.fields['category'].queryset = Category.objects.filter(event=event)
        self.fields['tags'].queryset = Tag.objects.filter(event=event)

    class Meta:
        model = Programme
        fields = (
            'title',
            'description',
            'form_used',
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
            'rerun',
            'room_requirements',
            'requested_time_slot',
            'notes_from_host',
        )


class ProgrammeOfferForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(ProgrammeOfferForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        for field_name in [
            'title',
            'description',
        ]:
            self.fields[field_name].required = True

        self.fields['category'].queryset = Category.objects.filter(event=event, public=True)

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            'title',
            'description',
            'category',
            'computer',
            'use_audio',
            'use_video',
            'number_of_microphones',
            'tech_requirements',
            'video_permission',
            'encumbered_content',
            'photography',
            'rerun',
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
            'rerun',
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
            'video_link',
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


def get_sired_invitation_formset(request, num_extra_invites):
    SiredInvitationFormset = modelformset_factory(Invitation,
        form=SiredInvitationForm,
        validate_max=True,
        extra=num_extra_invites,
        max_num=num_extra_invites,
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
    #     accepting_cold_offers_from = self.cleaned_data.get('accepting_cold_offers_from')
    #     accepting_cold_offers_until = self.cleaned_data.get('accepting_cold_offers_until')

    #     if accepting_cold_offers_from and accepting_cold_offers_until and accepting_cold_offers_from >= accepting_cold_offers_until:
    #         raise forms.ValidationError(_("The registration closing time must be after the registration opening time."))

    #     return accepting_cold_offers_until

    class Meta:
        model = ProgrammeEventMeta
        fields = (
            'public_from',
        )


class ProgrammeFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        is_own_programme = kwargs.pop('is_own_programme')

        super(ProgrammeFeedbackForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        if is_own_programme:
            self.fields['is_anonymous'].disabled = True
            self.fields['is_anonymous'].help_text = _('Because you are the host of this programme, you cannot leave your feedback anonymously.')

    class Meta:
        model = ProgrammeFeedback
        fields = (
            'feedback',
            'is_anonymous',
        )


class ColdOffersForm(forms.ModelForm):
    # XXX get a date picker
    accepting_cold_offers_from = forms.DateTimeField(
        required=False,
        label=_('Accepting cold offers from'),
    )
    accepting_cold_offers_until = forms.DateTimeField(
        required=False,
        label=_('Accepting cold offers until'),
        help_text=_("Format: YYYY-MM-DD HH:MM:SS"),
    )

    def __init__(self, *args, **kwargs):
        super(ColdOffersForm, self).__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    def clean_registration_closes(self):
        accepting_cold_offers_from = self.cleaned_data.get('accepting_cold_offers_from')
        accepting_cold_offers_until = self.cleaned_data.get('accepting_cold_offers_until')

        if accepting_cold_offers_from and accepting_cold_offers_until and accepting_cold_offers_from >= accepting_cold_offers_until:
            raise forms.ValidationError(_("The closing time must be after the opening time."))

        return accepting_cold_offers_until

    class Meta:
        model = ColdOffersProgrammeEventMetaProxy
        fields = (
            'accepting_cold_offers_from',
            'accepting_cold_offers_until',
        )
