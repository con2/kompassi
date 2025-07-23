from functools import wraps

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from kompassi.access.cbac import default_cbac_required
from kompassi.core.models import Event
from kompassi.core.utils.view_utils import get_event_and_organization

from .views.admin_menu_items import labour_admin_menu_items


def labour_admin_required(view_func):
    @wraps(view_func)
    @default_cbac_required
    def wrapper(request, *args, **kwargs):
        kwargs.pop("event_slug")
        event, _ = get_event_and_organization(request)
        if not event:
            raise Http404

        meta = event.labour_event_meta

        if not meta:
            messages.error(request, "Tämä tapahtuma ei käytä Kompassia työvoiman hallintaan.")
            return redirect("core_event_view", event.slug)

        vars = dict(
            event=event, admin_menu_items=labour_admin_menu_items(request, event), admin_title="Työvoiman hallinta"
        )

        return view_func(request, vars, event, *args, **kwargs)

    return wrapper


def labour_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        event = get_object_or_404(Event, slug=event_slug)
        meta = event.labour_event_meta

        if not meta:
            messages.error(request, "Tämä tapahtuma ei käytä Kompassia työvoiman hallintaan.")
            return redirect("core_event_view", event.slug)

        return view_func(request, event, *args, **kwargs)

    return wrapper
