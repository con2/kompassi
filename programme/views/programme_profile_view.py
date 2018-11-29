# encoding: utf-8

from django.shortcuts import render

from core.helpers import person_required

from ..models import Programme


@person_required
def programme_profile_view(request):
    person = request.user.person

    future_programmes = Programme.get_future_programmes(person)
    past_programmes = Programme.get_past_programmes(person)
    rejected_programmes = Programme.get_rejected_programmes(person)

    no_programmes = not any(i.exists() for i in (
        future_programmes,
        past_programmes,
        rejected_programmes,
    ))

    vars = dict(
        future_programmes=future_programmes,
        no_programmes=no_programmes,
        past_programmes=past_programmes,
        rejected_programmes=rejected_programmes,
    )

    return render(request, 'programme_profile_view.pug', vars)
