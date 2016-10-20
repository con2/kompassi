# encoding: utf-8

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

from ..helpers import intra_organizer_required
from ..models import Team


@intra_organizer_required
def intra_organizer_view(request, vars, event):
    meta = event.intra_event_meta
    teams = Team.objects.filter(event=event).prefetch_related('members')

    vars.update(
        teams=teams,
        unassigned_organizers=meta.unassigned_organizers,
        num_unassigned_organizers=len(meta.unassigned_organizers)
    )

    return render(request, 'intra_organizer_view.jade', vars)
