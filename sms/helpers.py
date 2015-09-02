# encoding: utf-8

from functools import wraps

from django.shortcuts import get_object_or_404


def sms_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        from core.models import Event
        from core.utils import login_redirect
        from .views import sms_admin_menu_items

        event = get_object_or_404(Event, slug=event_slug)
        meta = event.sms_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Kompassia tekstiviestien lähetykseen.")
            return redirect('core_event_view', event.slug)

        if not meta.is_user_admin(request.user):
            return login_redirect(request)

        vars = dict(
            event=event,
            meta=meta,
            admin_menu_items=sms_admin_menu_items(request, event),
            admin_title=u'Tekstiviestit'
        )

        return view_func(request, vars, event, *args, **kwargs)
    return wrapper
