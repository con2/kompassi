# encoding: utf-8

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404

from core.helpers import person_required

from ..helpers import programme_event_required
from ..models.hosts import Invitation


@programme_event_required
@person_required
def programme_accept_invitation_view(request, event, code):
    invitation = get_object_or_404(Invitation, programme__category__event=event, code=code)

    vars = dict(
    )

    return render(request, 'programme_accept_invitation_view.jade', vars)