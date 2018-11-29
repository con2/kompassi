# encoding: utf-8



from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from ipware.ip import get_ip

from core.helpers import person_required
from core.utils import initialize_form

from ..forms import ProgrammeFeedbackForm, AnonymousProgrammeFeedbackForm
from ..models import Programme
from ..helpers import programme_event_required


@programme_event_required
def programme_feedback_view(request, event, programme_id):
    programme = get_object_or_404(Programme, id=int(programme_id), category__event=event)

    if not programme.is_open_for_feedback:
        messages.error(request, _('You cannot leave feedback about a programme that has not yet been delivered.'))
        return redirect('core_event_view', event.slug)

    if request.user.is_authenticated:
        is_own_programme = request.user.person in programme.organizers.all()
        form = initialize_form(ProgrammeFeedbackForm, request, is_own_programme=is_own_programme)
    else:
        is_own_programme = False
        form = initialize_form(AnonymousProgrammeFeedbackForm, request)

    if request.method == 'POST':
        if form.is_valid():
            feedback = form.save(commit=False)

            if feedback.is_anonymous and is_own_programme:
                messages.error(request, _('You cannot leave anonymous feedback about your own programme.'))
            else:
                feedback.author = request.user.person if request.user.is_authenticated else None
                feedback.author_ip_address = get_ip(request) or ''
                feedback.programme = programme
                feedback.save()

                messages.success(request, _('Thank you for your feedback.'))
                return redirect('core_event_view', event.slug)
        else:
            messages.error(request, _('Please check the form.'))

    vars = dict(
        event=event,
        programme=programme,
        form=form,
    )

    return render(request, 'programme_feedback_view.pug', vars)
