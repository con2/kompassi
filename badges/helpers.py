# encoding: utf-8

from functools import wraps

from django.shortcuts import get_object_or_404


def badges_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        from core.models import Event
        from core.utils import login_redirect
        from .views import badges_admin_menu_items

        event = get_object_or_404(Event, slug=event_slug)
        meta = event.badges_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Kompassia kulkulupien hallintaan.")
            return redirect('core_event_view', event.slug)

        if not meta.is_user_admin(request.user):
            return login_redirect(request)

        vars = dict(
            event=event,
            meta=meta,
            admin_menu_items=badges_admin_menu_items(request, event),
            admin_title=u'Badgejen ja nimilistojen hallinta'
        )

        return view_func(request, vars, event, *args, **kwargs)
    return wrapper
