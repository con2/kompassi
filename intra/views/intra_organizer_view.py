# encoding: utf-8

from __future__ import unicode_literals

from collections import namedtuple

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

from core.models import Person
from labour.models import Signup

from ..helpers import intra_organizer_required
from ..models import Team


UnassignedOrganizer = namedtuple('UnassignedOrganizer', 'person signup')


@intra_organizer_required
def intra_organizer_view(request, vars, event):
    meta = event.intra_event_meta
    teams = Team.objects.filter(event=event).prefetch_related('members')

    unassigned_organizers = [
        UnassignedOrganizer(
            person=person,
            signup=Signup.objects.get(event=event, person=person)
        )

        for person in Person.objects.filter(
            user__groups=meta.organizer_group,
        ).exclude(
            user__person__team_memberships__team__event_id=event.id,
        )
    ]

    vars.update(
        teams=teams,
        unassigned_organizers=unassigned_organizers,
        num_unassigned_organizers=len(unassigned_organizers)
    )

    return render(request, 'intra_organizer_view.jade', vars)
