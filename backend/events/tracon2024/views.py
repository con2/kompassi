from django.db import models
from django.shortcuts import render
from django.utils.timezone import now

from access.cbac import default_cbac_required
from core.csv_export import csv_response
from core.models import Event
from event_log_v2.utils.emit import emit

from .models import Poison
from .proxies import SignupExtraAfterpartyProxy


@default_cbac_required
def tracon2024_afterparty_participants_view(request, event_slug):
    if event_slug != "tracon2024":
        raise NotImplementedError("This view is only available for tracon2024")

    event = Event.objects.get(slug=event_slug)

    participants = SignupExtraAfterpartyProxy.objects.filter(afterparty_participation=True)

    filename = "{event.slug}_afterparty_participants_{timestamp}.xlsx".format(
        event=event,
        timestamp=now().strftime("%Y%m%d%H%M%S"),
    )

    emit("core.person.exported", request=request)

    return csv_response(
        event,
        SignupExtraAfterpartyProxy,
        participants,
        dialect="xlsx",
        filename=filename,
        m2m_mode="separate_columns",
    )


@default_cbac_required
def tracon2024_afterparty_summary_view(request, event_slug):
    if event_slug != "tracon2024":
        raise NotImplementedError("This view is only available for tracon2024")

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

    return render(request, "tracon2024_afterparty_summary_view.pug", vars)
