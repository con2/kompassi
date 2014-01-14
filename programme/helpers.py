# encoding: utf-8

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404


def programme_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event, *args, **kwargs):
        from core.models import Event

        event = get_object_or_404(Event, slug=event)
        meta = event.programme_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä ConDB:tä ohjelman hallintaan.")
            return redirect('core_event_view', event.slug)

        if not meta.public or event.programme_event_meta.is_user_admin(request.user):
            messages.error(request, u"Tämän tapahtuman ohjelma ei ole vielä julkinen.")
            return redirect('core_event_view', event.slug)

        return view_func(request, event, *args, **kwargs)
    return wrapper
