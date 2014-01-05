from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import Event


def core_event_view(request, event):
    event = get_object_or_404(Event, slug=event)

    vars = dict(
        event=event,
        settings=settings
    )

    if 'labour' in settings.INSTALLED_APPS:
        from labour.models import EventMeta
        vars.update(
            labour_active_events=EventMeta.active_events
        )

    return render(request, 'core_event_view.jade', vars)