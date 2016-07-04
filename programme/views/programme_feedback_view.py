# encoding: utf-8

from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from ipware.ip import get_ip

from core.helpers import person_required
from core.utils import initialize_form

from ..forms import ProgrammeFeedbackForm
from ..models import Programme
from ..helpers import programme_event_required


@person_required
@programme_event_required
def programme_feedback_view(request, event, programme_id):
    programme = get_object_or_404(Programme, id=int(programme_id), category__event=event)

    if not programme.is_open_for_feedback:
        messages.error(request, _('This programme is not currently accepting feedback.'))
        return redirect('core_event_view', event.slug)

    form = initialize_form(ProgrammeFeedbackForm, request)

    if request.method == 'POST':
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.author = request.user.person
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

    return render(request, 'programme_feedback_view.jade', vars)
