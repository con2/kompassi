# encoding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Event
from .forms import PersonForm
from .helpers import initialize_form


def core_frontpage_view(request):
    vars = dict(
        settings=settings
    )

    if 'labour' in settings.INSTALLED_APPS:
        from labour.models import LabourEventMeta
        vars.update(
            events_registration_open=LabourEventMeta.events_registration_open(),
        )

    return render(request, 'core_frontpage_view.jade', vars)


def core_event_view(request, event):
    event = get_object_or_404(Event, slug=event)

    vars = dict(
        event=event,
        settings=settings,
    )

    if 'labour' in settings.INSTALLED_APPS:
        from labour.views import labour_event_box_context
        vars.update(labour_event_box_context(request, event))

    return render(request, 'core_event_view.jade', vars)


@login_required
@require_http_methods(['GET', 'POST'])
def core_profile_view(request):
    person = request.user.person
    form = initialize_form(PersonForm, request, instance=person, prefix='person')

    if request.method == 'POST':
        if form.is_valid():
            person = form.save()
            messages.success(request, u'Tiedot tallennettiin.')
        else:
            messages.success(request, u'Ole hyvä ja korjaa virheelliset kentät.')

    vars = dict(
        form=form
    )

    return render(request, 'core_profile_view.jade', vars)


def core_profile_menu_items(request):
    items = []

    if not request.user.is_authenticated():
        return items

    profile_url = reverse('core_profile_view')
    profile_active = request.path == profile_url
    profile_text = u'Omat tiedot'

    items.append((profile_active, profile_url, profile_text))

    if 'labour' in settings.INSTALLED_APPS:
        from labour.views import labour_profile_menu_items
        items.extend(labour_profile_menu_items(request))

    return items
