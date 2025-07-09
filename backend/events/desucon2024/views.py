from django.db import connection, models
from django.shortcuts import render

from access.cbac import default_cbac_required
from core.models import Event

from .models import GENDER_SEGREGATION_CHOICES, Poison


@default_cbac_required
def desucon2024_afterparty_summary_view(request, event_slug):
    if event_slug != "desucon2024":
        raise NotImplementedError("This view is only available for desucon2024")

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

    with connection.cursor() as cursor:
        cursor.execute(
            """
            select
                gender_segregation,
                count(*)
            from
                desucon2024_signupextra
            where
                afterparty_participation
            group by
                gender_segregation
            """
        )

        gender_segregation_counts = dict(cursor.fetchall())

    gender_segregation_map = dict(GENDER_SEGREGATION_CHOICES)
    gender_segregation = [(gender_segregation_map[k], v) for (k, v) in gender_segregation_counts.items()]

    vars = dict(
        event=event,
        poisons=poisons,
        gender_segregation=gender_segregation,
    )

    return render(request, "desucon2024_afterparty_summary_view.pug", vars)
