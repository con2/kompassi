from django.db.models import Q
from django.shortcuts import render
from django.utils.timezone import now

from kompassi.core.utils import groupby_strict, groups_of_n

from ..models import CarouselSlide, Event


def get_year(event):
    return event.start_time.year


def events(*args, **kwargs):
    return (
        Event.objects.filter(*args, **kwargs)
        .order_by("-start_time")
        .select_related("venue")
        .select_related("enrollmenteventmeta")
        .select_related("ticketseventmeta")
        .select_related("laboureventmeta")
        .select_related("programmeeventmeta")
    )


def core_frontpage_view(request, template="core_frontpage_view.pug", include_past_events=False):
    t = now()

    if include_past_events:
        past_events = events(public=True, end_time__lte=t)
    else:
        past_events = Event.objects.none()

    current_events = events(public=True, start_time__lte=t, end_time__gt=t)
    future_events = events((Q(start_time__gt=t) | Q(start_time__isnull=True)) & Q(public=True)).order_by("start_time")

    past_events_rows_by_year = [
        (year, list(groups_of_n(year_events, 4))) for (year, year_events) in groupby_strict(past_events, get_year)
    ]

    vars = dict(
        carousel_slides=CarouselSlide.get_active_slides(),
        current_events_rows=list(groups_of_n(current_events, 4)),
        future_events_rows=list(groups_of_n(future_events, 4)),
        past_events_rows_by_year=past_events_rows_by_year,
    )

    return render(request, template, vars)
