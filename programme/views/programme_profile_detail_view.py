# encoding: utf-8

from django.shortcuts import get_object_or_404, render

from core.helpers import person_required
from core.utils import initialize_form

from ..proxies.programme.profile import ProgrammeProfileProxy


@person_required
def programme_profile_detail_view(request, programme_id):
    programme = get_object_or_404(ProgrammeProfileProxy, id=int(programme_id), organizers=request.user.person)
    event = programme.category.event

    vars = dict(
        event=event,
        programme=programme,
    )

    return render(request, 'programme_profile_detail_view.jade', vars)