from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from kompassi.core.utils import groupby_strict

from ..models import Listing


def listings_listing_view(request, listing_hostname, include_past_events=False):
    listing = get_object_or_404(Listing, hostname=listing_hostname)
    t = now()

    if include_past_events:
        past_events = listing.get_events(public=True, end_time__lte=t)
    else:
        past_events = []

    current_events = listing.get_events(public=True, start_time__lte=t, end_time__gt=t)
    future_events = listing.get_events(public=True, start_time__gt=t)

    past_events_by_year = groupby_strict(past_events, lambda event: event.start_time.year)

    vars = dict(
        listing=listing,
        current_events=current_events,
        future_events=future_events,
        past_events_by_year=past_events_by_year,
        show_future_events_heading=future_events and (current_events or past_events),
        login_page=True,
    )

    return render(request, "listings_listing_view.pug", vars)
