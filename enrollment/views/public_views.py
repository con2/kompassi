from django.shortcuts import render

from ..helpers import enrollment_event_required

@enrollment_event_required
def enrollment_enroll_view(request, event_slug):

    vars = dict()

    return render(request, 'enrollment_enroll_view.jade', vars)
