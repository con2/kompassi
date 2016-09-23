from django.shortcuts import render


def enrollment_enroll_view(request, event_slug):

    vars = dict()

    return render(request, 'enrollment_enroll_view.jade', vars)
