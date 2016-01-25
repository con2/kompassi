# encoding: utf-8

from django.shortcuts import render

from core.helpers import person_required

from ..proxies.programme.profile import ProgrammeProfileProxy


@person_required
def programme_profile_view(request):
    programmes = ProgrammeProfileProxy.objects.filter(organizers=request.user.person)

    vars = dict(
        programmes=programmes,
    )

    return render(request, 'programme_profile_view.jade', vars)