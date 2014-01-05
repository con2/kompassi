from django.shortcuts import get_object_or_404, render

from core.models import Event

from .models import EventMeta
from .forms import SignupForm


def labour_signup_view(request, event):
    print event
    event = get_object_or_404(Event, slug=event)

    vars = dict(
        event=event,
        signup_form=SignupForm(),
        signup_extra_form=event.eventmeta.signup_extra_model.init_form()
    )

    return render(request, 'labour_signup.jade', vars)
