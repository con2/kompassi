from functools import wraps

from django.shortcuts import get_object_or_404, redirect

from .utils import login_redirect


def labour_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event, *args, **kwargs):
        from core.models import Event
        from .views import labour_admin_menu_items

        event = get_object_or_404(Event, slug=event)
        if not event.laboureventmeta.is_user_admin(request.user):
            return login_redirect(request)

        vars = dict(
            event=event,
            admin_menu_items=labour_admin_menu_items(request, event)
        )

        return view_func(request, vars, event, *args, **kwargs)
    return wrapper
