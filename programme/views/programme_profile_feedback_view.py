# encoding: utf-8



from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from core.helpers import person_required
from core.utils import initialize_form

from ..forms import ProgrammeFeedbackForm
from ..models import Programme
from ..helpers import programme_event_required


def programme_profile_feedback_view(request, programme_id):
    programme = get_object_or_404(Programme, id=int(programme_id))
    event = programme.event

    if not request.user.person in programme.organizers.all():
        messages.error(request, _('Only an organizer of the programme may view its feedback.'))
        return redirect('programme_profile_view')

    feedback = programme.visible_feedback

    vars = dict(
        event=event,
        programme=programme,
        feedback=feedback,
    )

    return render(request, 'programme_profile_feedback_view.pug', vars)
