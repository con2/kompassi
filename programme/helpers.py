# encoding: utf-8

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404


def programme_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        from core.models import Event

        event = get_object_or_404(Event, slug=event_slug)
        meta = event.programme_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Turskaa ohjelman hallintaan.")
            return redirect('core_event_view', event.slug)

        return view_func(request, event, *args, **kwargs)
    return wrapper


def public_programme_required(view_func):
    @wraps(view_func)
    @programme_event_required
    def wrapper(request, event, *args, **kwargs):
        meta = event.programme_event_meta

        if not (meta.public or meta.is_user_admin(request.user)):
            messages.error(request, u"Tämän tapahtuman ohjelma ei ole vielä julkinen.")
            return redirect('core_event_view', event.slug)

        return view_func(request, event, *args, **kwargs)
    return wrapper


def programme_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        from core.models import Event
        from core.utils import login_redirect
        from .views import programme_admin_menu_items

        event = get_object_or_404(Event, slug=event_slug)
        meta = event.programme_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Turskaa ohjelman hallintaan.")
            return redirect('core_event_view', event.slug)

        if not event.programme_event_meta.is_user_admin(request.user):
            return login_redirect(request)

        vars = dict(
            event=event,
            admin_menu_items=programme_admin_menu_items(request, event),
            admin_title=u'Ohjelman hallinta'
        )

        return view_func(request, vars, event, *args, **kwargs)
    return wrapper
