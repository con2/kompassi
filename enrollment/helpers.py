# encoding: utf-8

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from functools import wraps

from core.models import Event

def enrollment_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        event = get_object_or_404(Event, slug=event_slug)
        meta = event.enrollment_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Kompassia ilmoittautumisiin.")
            return redirect('core_event_view', event.slug)

        return view_func(request, event, *args, **kwargs)
    return wrapper
