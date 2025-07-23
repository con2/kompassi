from typing import Any

from django.conf import settings
from django.shortcuts import get_object_or_404, render

from kompassi.badges.views import badges_event_box_context
from kompassi.forms.views.forms_event_box_context import forms_event_box_context
from kompassi.intra.views import intra_event_box_context
from kompassi.labour.views import labour_event_box_context
from kompassi.program_v2.views.program_v2_event_box_context import program_v2_event_box_context
from kompassi.tickets_v2.views.tickets_v2_event_box_context import tickets_v2_event_box_context
from kompassi.zombies.enrollment.views import enrollment_event_box_context
from kompassi.zombies.programme.views.event_box_context import programme_event_box_context
from kompassi.zombies.tickets.views import tickets_event_box_context

from ..models import Event


def core_event_view(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)

    vars: dict[str, Any] = dict(
        event=event,
        settings=settings,
    )

    if event.enrollment_event_meta:
        vars.update(enrollment_event_box_context(request, event))

    if event.labour_event_meta:
        vars.update(labour_event_box_context(request, event))

    if event.programme_event_meta:
        vars.update(programme_event_box_context(request, event))

    if event.program_v2_event_meta:
        vars.update(program_v2_event_box_context(request, event))

    if event.tickets_event_meta:
        vars.update(tickets_event_box_context(request, event))

    if event.badges_event_meta:
        vars.update(badges_event_box_context(request, event))

    if event.intra_event_meta:
        vars.update(intra_event_box_context(request, event))

    if event.forms_event_meta:
        vars.update(forms_event_box_context(request, event))

    if event.tickets_v2_event_meta:
        vars.update(tickets_v2_event_box_context(request, event))

    return render(request, "core_event_view.pug", vars)
