# encoding: utf-8



from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Person, Organization, Event
from .utils import login_redirect, event_meta_property  # noqa
from .page_wizard import page_wizard_init, page_wizard_clear


def person_required(view_func):
    @login_required
    @wraps(view_func)
    def inner(request, *args, **kwargs):
        try:
            person = request.user.person  # noqa
        except Person.DoesNotExist:
            return login_redirect(request, view='core_personify_view')

        return view_func(request, *args, **kwargs)

    return inner


# XXX WIP
def app_admin_required(app_label, error_message='Tämä moduuli ei ole käytössä tälle tapahtumalle.'):
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
                messages.error(request, "Tämä tapahtuma ei käytä Kompassia työvoiman hallintaan.")
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
            event = get_object_or_404(Event, slug=event)
            meta = event.labour_event_meta

            if not meta:
                messages.error(request, "Tämä tapahtuma ei käytä Kompassia työvoiman hallintaan.")
                return redirect('core_event_view', event.slug)

            return view_func(request, event, *args, **kwargs)
        return inner
    return outer


def unperson_page_wizard(*pages):
    """
    @login_required
    @unperson_page_wizard('url_or_name', ...)
    def view_func(request):
        pass

    Directs any User without Person through a series of pages before letting them perform this view.
    """
    assert len(pages) >= 1

    def outer(view_func):
        @wraps(view_func)
        def inner(request, *args, **kwargs):
            assert request.user.is_authenticated

            try:
                person = request.user.person
            except Person.DoesNotExist:
                pages.append(view_func.__name__)

                page_wizard_init(request, pages)
                return redirect(pages[0])
            else:
                page_wizard_clear(request)
                return view_func(request, *args, **kwargs)

        return inner
    return outer

def public_organization_required(view_func):
    @wraps(view_func)
    def wrapper(request, organization_slug, *args, **kwargs):
        if request.user.is_staff:
            organization = get_object_or_404(Organization, slug=organization_slug)
            if not organization.public:
                messages.warning(request, 'Tämä yhdistys ei ole julkinen. Tämä sivu ei näy tavallisille käyttäjille.')
        else:
            organization = get_object_or_404(Organization, slug=organization_slug, public=True)

        return view_func(request, organization, *args, **kwargs)

    return wrapper
