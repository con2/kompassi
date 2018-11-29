# encoding: utf-8

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_safe

from core.utils import initialize_form

from ..helpers import programme_admin_required
from ..models import ProgrammeFeedback


@programme_admin_required
@require_safe
def programme_admin_feedback_view(request, vars, event):
    feedback = ProgrammeFeedback.get_visible_feedback_for_event(event)

    vars.update(
        feedback=feedback
    )

    return render(request, 'programme_admin_feedback_view.pug', vars)
