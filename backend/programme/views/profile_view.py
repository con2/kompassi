from django.conf import settings
from django.shortcuts import render

from core.helpers import person_required

from ..models import Programme


@person_required
def profile_view(request):
    person = request.user.person

    future_programmes = Programme.get_future_programmes(person)
    past_programmes = Programme.get_past_programmes(person)
    rejected_programmes = Programme.get_rejected_programmes(person)

    no_programmes = not any(
        i.exists()
        for i in (
            future_programmes,
            past_programmes,
            rejected_programmes,
        )
    )

    vars = dict(
        future_programmes=future_programmes,
        no_programmes=no_programmes,
        past_programmes=past_programmes,
        rejected_programmes=rejected_programmes,
        program_v2_profile_link=f"{settings.KOMPASSI_V2_BASE_URL}/profile/program",
    )

    return render(request, "programme_profile_view.pug", vars)
