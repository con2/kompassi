from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Event
from .forms import PersonForm

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
    event = get_object_or_404(Event, pk=event)

    vars = dict(
        event=event,
        settings=settings
    )

    return render(request, 'core_event_view.jade', vars)


@login_required
def core_profile_view(request):
    person = request.user.person

    vars = dict(
        person=person,
        person_form=PersonForm(person, prefix='person')
    )

    return render(request, 'labour_ownprofile_view.jade', vars)