from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import Event
from kompassi.core.utils import login_redirect

from .views.menu_items import intra_admin_menu_items, intra_organizer_menu_items


def intra_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        event = get_object_or_404(Event, slug=event_slug)
        meta = event.intra_event_meta

        if not meta:
            messages.error(request, _("This event does not use the organizer intranet."))
            return redirect("core_event_view", event.slug)

        return view_func(request, event, *args, **kwargs)

    return wrapper


def intra_organizer_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        event = get_object_or_404(Event, slug=event_slug)
        meta = event.intra_event_meta

        if not meta:
            messages.error(request, _("This event does not use the organizer intranet."))
            return redirect("core_event_view", event.slug)

        if not request.user.is_authenticated:
            return login_redirect(request)

        if not meta.is_user_allowed_to_access(request.user):
            messages.error(request, _("You do not have access to the organizer intranet."))
            return redirect("core_event_view", event.slug)

        if meta.is_user_admin(request.user):
            is_intra_admin = True
            menu_items = intra_admin_menu_items(request, event)
        else:
            is_intra_admin = False
            menu_items = intra_organizer_menu_items(request, event)

        vars = dict(
            event=event,
            meta=meta,
            admin_menu_items=menu_items,
            admin_title=_("Organizer intranet"),
            is_intra_organizer=True,
            is_intra_admin=is_intra_admin,
        )

        return view_func(request, vars, event, *args, **kwargs)

    return wrapper


def intra_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        event = get_object_or_404(Event, slug=event_slug)
        meta = event.intra_event_meta

        if not meta:
            messages.error(request, _("This event does not use the organizer intranet."))
            return redirect("core_event_view", event.slug)

        if not request.user.is_authenticated:
            return login_redirect(request)

        if not meta.is_user_admin(request.user):
            messages.error(request, _("You do not have administrator access to the organizer intranet."))
            return redirect("core_event_view", event.slug)

        menu_items = intra_admin_menu_items(request, event)

        vars = dict(
            event=event,
            meta=meta,
            admin_menu_items=menu_items,
            admin_title=_("Organizer intranet"),
            is_intra_organizer=True,
            is_intra_admin=True,
        )

        return view_func(request, vars, event, *args, **kwargs)

    return wrapper
