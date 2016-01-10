# encoding: utf-8

from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from core.models import Event
from core.sort_and_filter import Filter
from core.utils import login_redirect

from .models.constants import SIGNUP_STATE_NAMES
from .models import Signup


def labour_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        event = get_object_or_404(Event, slug=event_slug)
        meta = event.labour_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Turskaa työvoiman hallintaan.")
            return redirect('core_event_view', event.slug)

        if not event.labour_event_meta.is_user_admin(request.user):
            return login_redirect(request)

        vars = dict(
            event=event,
            admin_menu_items=labour_admin_menu_items(request, event),
            admin_title=u'Työvoiman hallinta'
        )

        return view_func(request, vars, event, *args, **kwargs)
    return wrapper


def labour_supervisor_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        event = get_object_or_404(Event, slug=event_slug)
        meta = event.labour_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Turskaa työvoiman hallintaan.")
            return redirect('core_event_view', event.slug)

        if not event.labour_event_meta.is_user_supervisor(request.user):
            return login_redirect(request)

        return view_func(request, event, *args, **kwargs)
    return wrapper


def labour_event_required(view_func):
    @wraps(view_func)
    def wrapper(request, event_slug, *args, **kwargs):
        event = get_object_or_404(Event, slug=event_slug)
        meta = event.labour_event_meta

        if not meta:
            messages.error(request, u"Tämä tapahtuma ei käytä Turskaa työvoiman hallintaan.")
            return redirect('core_event_view', event.slug)

        return view_func(request, event, *args, **kwargs)
    return wrapper


class SignupStateFilter(Filter):
    def __init__(self, *args, **kwargs):
        super(SignupStateFilter, self).__init__(*args, **kwargs)

        for state_slug in SIGNUP_STATE_NAMES.iterkeys():
            self._add_state(state_slug)

    def _add_state(self, state):
        """
        Add a state to the filter. Name defaults to the long name for the state.

        :param state: State mnemonic.
        :param name: Name, or None.
        :return: This object.
        """
        self.add(state, SIGNUP_STATE_NAMES[state], Signup.get_state_query_params(state))


# circular import
from .views.admin_views import labour_admin_menu_items
