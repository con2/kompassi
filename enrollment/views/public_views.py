from core.helpers import person_required

from django.shortcuts import render

from ..helpers import enrollment_event_required
from ..models import Enrollment

@enrollment_event_required
@person_required
def enrollment_enroll_view(request, event_slug):

    already_enrolled = Enrollment.objects.filter(
        event=event_slug,
        person=request.user.person,
    ).exists()

    vars = dict(
        already_enrolled=already_enrolled,
    )

    return render(request, 'enrollment_enroll_view.jade', vars)
