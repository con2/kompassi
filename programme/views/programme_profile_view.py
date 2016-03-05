# encoding: utf-8

from django.shortcuts import render

from core.helpers import person_required

from ..proxies.programme.profile import Programme


@person_required
def programme_profile_view(request):
    person = request.user.person

    editable_programmes = Programme.get_editable_programmes(person)
    published_programmes = Programme.get_published_programmes(person)
    rejected_programmes = Programme.get_rejected_programmes(person)

    no_programmes = not any(i.exists() for i in (
        editable_programmes,
        published_programmes,
        rejected_programmes,
    ))

    vars = dict(
        editable_programmes=editable_programmes,
        no_programmes=no_programmes,
        published_programmes=published_programmes,
        rejected_programmes=rejected_programmes,
    )

    return render(request, 'programme_profile_view.jade', vars)