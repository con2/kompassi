from django import forms
from django.utils.translation import gettext_lazy as _

from core.utils import (
    format_datetime,
    horizontal_form_helper,
)

from ..models import (
    AllRoomsPseudoView,
    AlternativeProgrammeForm,
    AlternativeProgrammeFormMixin,
    Category,
    FreeformOrganizer,
    Programme,
    ProgrammeEventMeta,
    ProgrammeRole,
    Role,
    Tag,
)
from ..models.programme import START_TIME_LABEL
from ..proxies.programme_event_meta.cold_offers import ColdOffersProgrammeEventMetaProxy


class ProgrammeAdminCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields["form_used"].queryset = AlternativeProgrammeForm.objects.filter(event=event)
        self.fields["form_used"].help_text = _(
            "Select the form that will be used to edit the information of this programme. "
            "If this field is left blank, the default form will be used. "
            "Some events do not offer a choice of different forms, in which case "
            "this field will not have options and the default form will always be used. "
        )

        self.fields["category"].queryset = Category.objects.filter(event=event)
        self.fields["tags"].queryset = Tag.objects.filter(event=event)

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "form_used",
            "category",
            "tags",
        )

        widgets = dict(
            tags=forms.CheckboxSelectMultiple,
        )


class ProgrammeOfferForm(forms.ModelForm, AlternativeProgrammeFormMixin):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")
        if "admin" in kwargs:
            admin = kwargs.pop("admin")
        else:
            admin = False

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        for field_name in [
            "title",
        ]:
            self.fields[field_name].required = True

        if not admin:
            for field_name in [
                "description",
                "video_permission",
                "stream_permission",
                "photography",
                "rerun",
                "encumbered_content",
            ]:
                self.fields[field_name].required = True

        self.fields["category"].queryset = Category.objects.filter(event=event, public=True)

    def get_excluded_field_defaults(self):
        return dict()

    class Meta:
        model = Programme
        fields = (
            "title",
            "description",
            "category",
            "computer",
            "use_audio",
            "use_video",
            "number_of_microphones",
            "tech_requirements",
            "video_permission",
            "stream_permission",
            "encumbered_content",
            "photography",
            "rerun",
            "room_requirements",
            "requested_time_slot",
            "notes_from_host",
        )


ProgrammeSelfServiceForm = ProgrammeOfferForm


class ProgrammeInternalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = Programme
        fields = ("notes",)


class ScheduleForm(forms.ModelForm):
    start_time = forms.ChoiceField(choices=[], label=START_TIME_LABEL, required=False)

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields["length"].widget.attrs["min"] = 0
        self.fields["room"].queryset = event.rooms.all()

        self.fields["start_time"].choices = [("", "---------")] + [
            (start_time, format_datetime(start_time)) for start_time in AllRoomsPseudoView(event).start_times()
        ]

        self.fields["tags"].queryset = Tag.objects.filter(event=event)

    def clean_start_time(self):
        start_time = self.cleaned_data.get("start_time")

        if start_time == "":
            start_time = None

        return start_time

    class Meta:
        model = Programme
        fields = (
            "state",
            "frozen",
            "room",
            "start_time",
            "length",
            "video_link",
            "signup_link",
            "tags",
        )

        widgets = dict(
            tags=forms.CheckboxSelectMultiple,
        )


class FreeformOrganizerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = FreeformOrganizer
        fields = ("text",)


class IdForm(forms.Form):
    id = forms.IntegerField()


class ChangeHostRoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        self.fields["role"].queryset = Role.objects.filter(personnel_class__event=event)

    class Meta:
        model = ProgrammeRole
        fields = (
            "role",
            "extra_invites",
        )


class PublishForm(forms.ModelForm):
    public_from = forms.DateTimeField(
        required=False,
        label=_("Public from"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = ProgrammeEventMeta
        fields = ("public_from",)


class ColdOffersForm(forms.ModelForm):
    # XXX get a date picker
    accepting_cold_offers_from = forms.DateTimeField(
        required=False,
        label=_("Accepting cold offers from"),
    )
    accepting_cold_offers_until = forms.DateTimeField(
        required=False,
        label=_("Accepting cold offers until"),
        help_text=_("Format: YYYY-MM-DD HH:MM:SS"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    def clean_registration_closes(self):
        accepting_cold_offers_from = self.cleaned_data.get("accepting_cold_offers_from")
        accepting_cold_offers_until = self.cleaned_data.get("accepting_cold_offers_until")

        if (
            accepting_cold_offers_from
            and accepting_cold_offers_until
            and accepting_cold_offers_from >= accepting_cold_offers_until
        ):
            raise forms.ValidationError(_("The closing time must be after the opening time."))

        return accepting_cold_offers_until

    class Meta:
        model = ColdOffersProgrammeEventMetaProxy
        fields = (
            "accepting_cold_offers_from",
            "accepting_cold_offers_until",
        )
