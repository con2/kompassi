from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import Event


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


def core_login_view(request):
    vars = dict(
        form=LoginForm(request.POST)
    )




def core_event_view(request, event):
    event = get_object_or_404(Event, pk=event)

    vars = dict(
        event=event,
        settings=settings
    )

    return render(request, 'core_event_view.jade', vars)