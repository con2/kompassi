# encoding: utf-8

from functools import wraps

from django.contrib.auth.decorators import login_required

from .models import Person
from .utils import login_redirect

def person_required(view_func):
    @login_required
    @wraps(view_func)
    def inner(request, *args, **kwargs):
        try:
            person = request.user.person
        except Person.DoesNotExist:
            return login_redirect(request, view='core_personify_view')

        return view_func(request, *args, **kwargs)

    return inner


# XXX WIP
def app_admin_required(app_label, error_message=u'Tämä moduuli ei ole käytössä tälle tapahtumalle.'):
    def outer(view_func):
        @wraps(view_func)
        def inner(request, event, *args, **kwargs):
            from core.models import Event
            from core.utils import login_redirect
            from .views import labour_admin_menu_items

            event = get_object_or_404(Event, slug=event)
            event_meta_name = '{app_label}_event_meta'.format(app_label=app_label)
            meta = getattr(event, event_meta_name, None)

            if not meta:
                messages.error(request, u"Tämä tapahtuma ei käytä Turskaa työvoiman hallintaan.")
                return redirect('core_event_view', event.slug)

            if not meta.is_user_admin(request.user):
                return login_redirect(request)

            vars = dict(
                event=event,
                # XXX this must differ from app to app?
                admin_menu_items=labour_admin_menu_items(request, event)
            )

            return view_func(request, vars, event, *args, **kwargs)
        return inner
    return outer


def app_event_required(app_label, error_message):
    def outer(view_func):
        @wraps(view_func)
        def inner(request, event, *args, **kwargs):
            from core.models import Event

            event = get_object_or_404(Event, slug=event)
            meta = event.labour_event_meta

            if not meta:
                messages.error(request, u"Tämä tapahtuma ei käytä Turskaa työvoiman hallintaan.")
                return redirect('core_event_view', event.slug)

            return view_func(request, event, *args, **kwargs)
        return inner
    return outer
