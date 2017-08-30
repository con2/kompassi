from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import Layout, Fieldset

from core.models import Person
from core.utils import horizontal_form_helper, indented_without_label, ensure_user_is_member_of_group
from labour.models.constants import JOB_TITLE_LENGTH

from .models import TeamMember, Team


class TeamMemberForm(forms.ModelForm):
    job_title = forms.CharField(
        max_length=JOB_TITLE_LENGTH,
        label=_('Job title'),
        required=False,
        help_text=_(
            'This corresponds to the job title field in the volunteer worker management. This is what is '
            'printed in this person\'s badge, if they will receive one. '
            'If unset, a default value based on the job category will be used for the badge.'
        ),
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        instance = kwargs.get('instance')
        initial = kwargs.setdefault('initial', dict())
        if instance:
            initial['job_title'] = instance.signup.job_title

        super(TeamMemberForm, self).__init__(*args, **kwargs)

        if not instance:
            del self.fields['job_title']
            del self.fields['override_job_title']

        self.fields['team'].queryset = Team.objects.filter(event=event)
        self.fields['person'].queryset = Person.objects.filter(
            user__groups=event.intra_event_meta.organizer_group,
        )

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'team',
            'person',
            Fieldset(_('Presentation'),
                'job_title', # not part of the model
                'override_job_title',
                'override_name_display_style',
            ),
            Fieldset(_('Additional options'),
                'is_primary_team',
                'is_team_leader',
                'is_shown_internally',
                'is_shown_publicly',
                'is_group_member',
            ),
        )

    def save(self, *args, **kwargs):
        ret = super(TeamMemberForm, self).save(*args, **kwargs)

        if 'job_title' in self.cleaned_data:
            signup = self.instance.signup
            signup.job_title = self.cleaned_data['job_title']
            signup.save()
            signup.apply_state()

        return ret

    class Meta:
        model = TeamMember
        fields = (
            'team',
            'person',
            'override_job_title',
            'is_primary_team',
            'is_team_leader',
            'is_shown_internally',
            'is_shown_publicly',
            'is_group_member',
            'override_name_display_style',
        )


SUPPORTED_APPS = [
    'labour',
    'programme',
    'tickets',
    'badges',
    'intra',
]


class PrivilegesForm(forms.Form):
    labour = forms.BooleanField(
        required=False,
        label=_('Labour admin'),
        help_text=_(
            'The Labour admin can approve or reject volunteer worker applications, assign workers to shifts etc.'
        ),
    )
    programme = forms.BooleanField(
        required=False,
        label=_('Programme admin'),
        help_text=_(
            'The Programme admin can approve or reject programme offers, modify the event programme schedule etc.'
        ),
    )
    tickets = forms.BooleanField(
        required=False,
        label=_('Tickets admin'),
        help_text=_(
            'The Tickets admin can view, cancel and modify ticket orders and exchange electronic tickets.'
        ),
    )
    badges = forms.BooleanField(
        required=False,
        label=_('Badges admin'),
        help_text=_('The Badges admin can add and revoke badges and export entrance lists.'),
    )
    intra = forms.BooleanField(
        required=False,
        label=_('Intra admin'),
        help_text=_('The Intra admin can assign organizers to teams and manage these privileges.'),
    )

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        self.active_apps = self.get_active_apps(event)

        if 'instance' in kwargs:
            assert 'initial' not in kwargs
            team_member = kwargs.pop('instance')
            initial = dict(
                (app_label, event.app_event_meta(app_label).is_user_in_admin_group(team_member.person.user))
                for app_label in self.active_apps
            )
            kwargs['initial'] = initial

        super(PrivilegesForm, self).__init__(*args, **kwargs)

        for app_label in SUPPORTED_APPS:
            if app_label not in self.active_apps:
                del self.fields[app_label]

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

        layout_fields = [indented_without_label(app_label) for app_label in self.active_apps]
        self.helper.layout = Layout(Fieldset(_('Privileges'), *layout_fields))

    @staticmethod
    def get_active_apps(event):
        return [app_label for app_label in SUPPORTED_APPS if event.app_event_meta(app_label)]

    def save(self, team_member):
        if 'background_tasks' in settings.INSTALLED_APPS:
            from .tasks import privileges_form_save
            privileges_form_save.delay(team_member.id, self.cleaned_data)
        else:
            self._save(team_member, self.cleaned_data)

    @classmethod
    def _save(cls, team_member, cleaned_data):
        event = team_member.event

        for app_label in cls.get_active_apps(event):
            ensure_user_is_member_of_group(
                team_member.person.user,
                event.app_event_meta(app_label).admin_group,
                cleaned_data[app_label]
            )

        return team_member
