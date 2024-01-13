from django.shortcuts import render
from django.views.decorators.http import require_safe

from ..helpers import programme_admin_required
from ..models import ProgrammeFeedback


@programme_admin_required
@require_safe
def admin_feedback_view(request, vars, event):
    feedback = ProgrammeFeedback.get_visible_feedback_for_event(event)

    vars.update(feedback=feedback)

    return render(request, "programme_admin_feedback_view.pug", vars)
