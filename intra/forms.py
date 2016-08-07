# encoding: utf-8

from __future__ import unicode_literals

from django import forms

from core.models import Person
from core.utils import horizontal_form_helper

from .models import TeamMember, Team


class TeamMemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')

        super(TeamMemberForm, self).__init__(*args, **kwargs)

        self.fields['team'].queryset = Team.objects.filter(event=event)
        self.fields['person'].queryset = Person.objects.filter(
            user__groups=event.intra_event_meta.organizer_group,
        )

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = TeamMember
        fields = (
            'team',
            'person',
            'is_primary_team',
            'is_team_leader',
            'is_shown_internally',
            'is_shown_publicly',
            'is_group_member',
        )
