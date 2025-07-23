from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from kompassi.core.helpers import person_required

from ..models import Programme


@person_required
def profile_feedback_view(request, programme_id):
    programme = get_object_or_404(Programme, id=int(programme_id))
    event = programme.event

    if request.user.person not in programme.organizers.all():
        messages.error(request, _("Only an organizer of the programme may view its feedback."))
        return redirect("programme:profile_view")

    feedback = programme.visible_feedback

    vars = dict(
        event=event,
        programme=programme,
        feedback=feedback,
    )

    return render(request, "programme_profile_feedback_view.pug", vars)
