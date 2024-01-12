from collections import Counter

from django.db import models
from django.utils.timezone import now
from django.shortcuts import render

from core.csv_export import csv_response
from core.models import Event
from event_log.utils import emit
from labour.helpers import labour_admin_required

from .proxies import SignupExtraAfterpartyProxy
from .models import Poison


@labour_admin_required
def tracon2019_afterparty_participants_view(request, vars, event):
    assert event.slug == "tracon2019"

    participants = SignupExtraAfterpartyProxy.objects.filter(afterparty_participation=True)

    filename = "{event.slug}_afterparty_participants_{timestamp}.xlsx".format(
        event=event,
        timestamp=now().strftime("%Y%m%d%H%M%S"),
    )

    emit("core.person.exported", request=request, event=event)

    return csv_response(
        event,
        SignupExtraAfterpartyProxy,
        participants,
        dialect="xlsx",
        filename=filename,
        m2m_mode="separate_columns",
    )


def count_passengers(signup_extras, field_name):
    # wrong: returns one row per SignupExtra
    # return signup_extras.values_list(field_name).annotate(
    #     passengers=Case(
    #         When(afterparty_participation=True, then=1),
    #         default=0,
    #         output_field=IntegerField(),
    #     ),
    # )

    return list(Counter(signup_extras.values_list(field_name, flat=True)).items())


def tracon2019_afterparty_summary_view(request, event_slug):
    assert event_slug == "tracon2019"
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

    return render(request, "tracon2019_afterparty_summary_view.pug", vars)
