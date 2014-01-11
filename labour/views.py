from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from core.models import Event

from .models import LabourEventMeta
from .forms import SignupForm


@login_required
def labour_signup_view(request, event):
    event = get_object_or_404(Event, slug=event)

    vars = dict(
        event=event,
        signup_form=SignupForm(),
        signup_extra_form=event.laboureventmeta.signup_extra_model.init_form(),
    )

    return render(request, 'labour_signup.jade', vars)

def labour_event_box_context(request, event):
    if request.user.is_authenticated():
        current_user_signed_up = event.laboureventmeta.is_person_signed_up(request.user.person)
    else:
        current_user_signed_up = False

    return dict(current_user_signed_up=current_user_signed_up)