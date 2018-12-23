# encoding: utf-8

from itertools import groupby
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from core.utils import groupby_strict


def programme_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        from core.models import Event

        event = get_object_or_404(Event, slug=event_slug)
        meta = event.programme_event_meta

        if not meta:
            messages.error(request, "Tämä tapahtuma ei käytä tätä sivustoa ohjelman hallintaan.")
            return redirect('core_event_view', event.slug)

        return view_func(request, event, *args, **kwargs)
    return wrapper


def public_programme_required(view_func):
    @wraps(view_func)
    @programme_event_required
    def wrapper(request, event, *args, **kwargs):
        meta = event.programme_event_meta

        if not meta.is_public:
            if not meta.is_user_admin(request.user):
                messages.error(request, "Tämän tapahtuman ohjelma ei ole vielä julkinen.")
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
            messages.error(request, "Tämä tapahtuma ei käytä tätä sivustoa ohjelman hallintaan.")
            return redirect('core_event_view', event.slug)

        if not event.programme_event_meta.is_user_admin(request.user):
            return login_redirect(request)

        vars = dict(
            event=event,
            admin_menu_items=programme_admin_menu_items(request, event),
            admin_title='Ohjelman hallinta'
        )

        return view_func(request, vars, event, *args, **kwargs)
    return wrapper


def group_programmes_by_start_time(programmes):
    programmes_by_start_time = groupby_strict(programmes, lambda p: p.start_time)
    return [
        (start_time, None, [(programme, None) for programme in programmes])
        for (start_time, programmes) in programmes_by_start_time
    ]
