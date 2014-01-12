from functools import wraps

from django.http import HttpResponseForbidden


def labour_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event, *args, **kwargs):
        event = get_object_or_404(Event, slug=event)
        if not event.laboureventmeta.is_user_admin(request.user):
            return HttpResponseForbidden()

        return view_func(request, event, *args, **kwargs)
