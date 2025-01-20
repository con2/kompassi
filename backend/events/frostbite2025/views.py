from django.db import models
from django.shortcuts import render

from access.cbac import default_cbac_required
from core.models import Event

from .models import Poison


@default_cbac_required
def frostbite2025_afterparty_summary_view(request, event_slug):
    if event_slug != "frostbite2025":
        raise NotImplementedError("This view is only available for frostbite2025")

    event = Event.objects.get(slug=event_slug)

    poisons = Poison.objects.all().annotate(
        victims=models.Sum(
            models.Case(
                models.When(signupextra__afterparty_participation=True, then=1),
                default=0,
                output_field=models.IntegerField(),
            )
        )
    )

    vars = dict(
        event=event,
        poisons=poisons,
    )

    return render(request, "frostbite2025_afterparty_summary_view.pug", vars)
