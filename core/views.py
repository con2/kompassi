from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
            events_registration_open=LabourEventMeta.events_registration_open()
        )

    return render(request, 'core_frontpage_view.jade', vars)


def core_event_view(request, event):
    from labour.views import labour_event_box_context

    event = get_object_or_404(Event, pk=event)

    vars = dict(
        event=event,
        settings=settings,
        **labour_event_box_context(request, event)
    )

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

    vars = dict(
        person=person,
        form=form
    )

    return render(request, 'core_profile_view.jade', vars)