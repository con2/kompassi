# encoding: utf-8

from core.helpers import person_required
from core.models import Event
from core.utils import initialize_form

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import EnrollmentForm
from ..helpers import enrollment_event_required
from ..models import Enrollment

@enrollment_event_required
@person_required
def enrollment_enroll_view(request, event):

    already_enrolled = Enrollment.objects.filter(
        event=event,
        person=request.user.person,
    ).exists()

    mandatory_information_missing = not (
        request.user.person
    )

    form = initialize_form(EnrollmentForm, request)

    if request.method == 'POST':
        if already_enrolled:
            messages.error(request, u'Olet jo ilmoittautunut tähän tapahtumaan.')
            return redirect('core_event_view', event.slug)
        elif mandatory_information_missing:
            messages.error(request, u'Ilmoittautumisestasi puuttuu pakollisia tietoja.')
        elif not form.is_valid():
            messages.error(request, u'Tarkista lomakkeen tiedot.')
        else:
            enrollment = form.save(commit=False)
            enrollment.event = event
            enrollment.person = request.user.person
            enrollment.save()

            messages.success(request,
                u'Kiitos ilmoittautumisestasi!'
            )
            return redirect('core_event_view', event.slug)

    vars = dict(
        already_enrolled=already_enrolled,
        event_slug = event,
        form=form,
        mandatory_information_missing=mandatory_information_missing,
    )

    return render(request, 'enrollment_enroll_view.jade', vars)
