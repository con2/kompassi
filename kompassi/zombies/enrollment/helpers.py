from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import Event


def enrollment_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        event = get_object_or_404(Event, slug=event_slug)
        meta = event.enrollment_event_meta

        if not meta:
            messages.error(request, _("This event does not use this site to manage enrollment."))
            return redirect("core_event_view", event.slug)

        return view_func(request, event, *args, **kwargs)

    return wrapper


def enrollment_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        from kompassi.core.models import Event
        from kompassi.core.utils import login_redirect

        from .views import enrollment_admin_menu_items

        event = get_object_or_404(Event, slug=event_slug)
        meta = event.enrollment_event_meta

        if not meta:
            messages.error(request, _("This event does not use this site to manage enrollment."))
            return redirect("core_event_view", event.slug)

        if not request.user.is_authenticated:
            return login_redirect(request)

        if not event.enrollment_event_meta.is_user_admin(request.user):
            messages.error(request, _("You are not allowed to manage enrollment for this event."))
            return redirect("core_event_view", event.slug)

        vars = dict(
            admin_menu_items=enrollment_admin_menu_items(request, event),
            admin_title=_("Manage enrollment"),
            event=event,
            meta=meta,
        )

        return view_func(request, vars, event, *args, **kwargs)

    return wrapper
