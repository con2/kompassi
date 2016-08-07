# encoding: utf-8

from __future__ import unicode_literals

from django.shortcuts import render

from ..helpers import intra_organizer_required
from ..models import Team


@intra_organizer_required
def intra_organizer_view(request, vars, event):
    teams = Team.objects.filter(event=event).prefetch_related('members')

    vars.update(
        teams=teams
    )
    return render(request, 'intra_organizer_view.jade', vars)
