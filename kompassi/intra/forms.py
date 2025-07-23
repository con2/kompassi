from __future__ import annotations

from typing import Any

from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from kompassi.access.models.cbac_entry import CBACEntry
from kompassi.core.models import Event, Person
from kompassi.core.utils import ensure_user_is_member_of_group, horizontal_form_helper, indented_without_label
from kompassi.labour.models.constants import JOB_TITLE_LENGTH

from .constants import SUPPORTED_APPS
from .models import Team, TeamMember


class TeamMemberForm(forms.ModelForm):
    job_title = forms.CharField(
        max_length=JOB_TITLE_LENGTH,
        label=_("Job title"),
        required=False,
        help_text=_(
            "This corresponds to the job title field in the volunteer worker management. This is what is "
            "printed in this person's badge, if they will receive one. "
            "If unset, a default value based on the job category will be used for the badge."
        ),
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event")

        instance = kwargs.get("instance")
        initial = kwargs.setdefault("initial", dict())
        if instance:
            initial["job_title"] = instance.signup.job_title

        super().__init__(*args, **kwargs)

        if not instance:
            # simplify form for new users
            for field_name in [
                "job_title",
                "override_job_title",
            ]:
                del self.fields[field_name]

        self.fields["team"].queryset = Team.objects.filter(event=event)  # type: ignore
        self.fields["person"].queryset = Person.objects.filter(  # type: ignore
            user__groups=event.intra_event_meta.organizer_group,
        )

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        layout_parts: list[Any] = [
            "team",
            "person",
        ]

        if instance:
            layout_parts.append(
                Fieldset(
                    _("Presentation"),
                    "job_title",
                    "override_job_title",
                )
            )

            layout_parts.append(
                Fieldset(
                    _("Additional options"),
                    "is_team_leader",
                    "is_shown_publicly",
                )
            )
        else:
            layout_parts.extend(
                (
                    "is_team_leader",
                    "is_shown_publicly",
                )
            )

        self.helper.layout = Layout(*layout_parts)

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)

        if "job_title" in self.cleaned_data:
            signup = self.instance.signup
            signup.job_title = self.cleaned_data["job_title"]
            signup.save()
            signup.apply_state()

        return ret

    class Meta:
        model = TeamMember
        fields = (
            "team",
            "person",
            "override_job_title",
            "is_team_leader",
            "is_shown_publicly",
        )


class PrivilegesForm(forms.Form):
    labour = forms.BooleanField(
        required=False,
        label=_("Labour admin"),
        help_text=_(
            "The Labour admin can approve or reject volunteer worker applications, assign workers to shifts etc."
        ),
    )
    programme = forms.BooleanField(
        required=False,
        label=_("Programme admin"),
        help_text=_(
            "The Programme admin can approve or reject programme offers, modify the event programme schedule etc."
        ),
    )
    program_v2 = forms.BooleanField(
        required=False,
        label=_("Program v2 admin"),
        help_text=_(
            "The Program admin can approve or reject program offers, modify the event program schedule etc. in Program V2."
        ),
    )
    tickets = forms.BooleanField(
        required=False,
        label=_("Tickets admin"),
        help_text=_("The Tickets admin can view, cancel and modify ticket orders and exchange electronic tickets."),
    )
    tickets_v2 = forms.BooleanField(
        required=False,
        label=_("Tickets v2 admin"),
        help_text=_("The Tickets admin can view, cancel and modify ticket orders and exchange electronic tickets."),
    )
    badges = forms.BooleanField(
        required=False,
        label=_("Badges admin"),
        help_text=_("The Badges admin can add and revoke badges and export entrance lists."),
    )
    intra = forms.BooleanField(
        required=False,
        label=_("Intra admin"),
        help_text=_("The Intra admin can assign organizers to teams and manage these privileges."),
    )
    forms = forms.BooleanField(
        required=False,
        label=_("Surveys admin"),
        help_text=_("The Surveys admin can manage surveys and view survey responses."),
    )

    def __init__(self, *args, **kwargs):
        if "initial" in kwargs:
            raise AssertionError('"initial" must not be passed to PrivilegesForm')

        self.event = kwargs.pop("event")
        self.user = kwargs.pop("user")
        self.active_apps = self.event.intra_event_meta.get_active_apps()

        kwargs["initial"] = {
            app_label: self.event.get_app_event_meta(app_label).is_user_in_admin_group(self.user)
            for app_label in self.active_apps
        }

        super().__init__(*args, **kwargs)

        for app_label in SUPPORTED_APPS:
            if app_label not in self.active_apps:
                del self.fields[app_label]

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        layout_fields = [indented_without_label(app_label) for app_label in self.active_apps]
        self.helper.layout = Layout(Fieldset(_("Privileges"), *layout_fields))

    @classmethod
    def save(cls, forms: list[PrivilegesForm]):
        from .tasks import privileges_form_save

        if not forms:
            return

        event = forms[0].event
        data = [(form.user.id, form.cleaned_data) for form in forms]
        privileges_form_save.delay(event.id, data)  # type: ignore

    @classmethod
    def _save(cls, event: Event, data: list[tuple[AbstractUser, dict[str, bool]]]):
        for user, is_member_by_app in data:
            for app_label in event.intra_event_meta.get_active_apps():
                ensure_user_is_member_of_group(
                    user,
                    event.get_app_event_meta(app_label).admin_group,
                    is_member_by_app[app_label],
                )

        CBACEntry.ensure_admin_group_privileges_for_event(event)

    @property
    def signup(self):
        from kompassi.labour.models import Signup

        return Signup.objects.filter(event=self.event, person=self.user.person).first()
