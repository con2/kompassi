# encoding: utf-8

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from core.models import Event
from core.helpers import initialize_form

from .models import LabourEventMeta
from .forms import SignupForm


@login_required
@require_http_methods(['GET', 'POST'])
def labour_signup_view(request, event):
    event = get_object_or_404(Event, slug=event)
    signup = event.laboureventmeta.get_signup_for_person(request.user.person)

    if signup.pk is not None:
        extra = signup.signup_extra
        messages.info(request, u'Olet jo ilmoittautunut tähän tapahtumaan. Voit halutessasi muuttaa ilmoittautumisesi tietoja.')
    else:
        extra = None

    SignupExtraForm = event.laboureventmeta.signup_extra_model.get_form_class()
    signup_form = initialize_form(SignupForm, request, instance=signup, prefix='signup')
    signup_extra_form = initialize_form(SignupExtraForm, request, instance=extra, prefix='extra')

    if request.method == 'POST':
        if signup_form.is_valid() and signup_extra_form.is_valid():
            signup_form.save()
            signup_extra_form.save()

            messages.success(u'Kiitos ilmoittautumisestasi!')

    vars = dict(
        event=event,
        signup_form=signup_form,
        signup_extra_form=signup_extra_form,
    )

    return render(request, 'labour_signup_view.jade', vars)

def labour_event_box_context(request, event):
    if request.user.is_authenticated():
        current_user_signed_up = event.laboureventmeta.is_person_signed_up(request.user.person)
    else:
        current_user_signed_up = False

    return dict(current_user_signed_up=current_user_signed_up)