# encoding: utf-8

from __future__ import unicode_literals

from core.models import Person

from ..models import Enrollment


def enrollment_event_box_context(request, event):
    enrollment = None
    is_enrollment_admin = False

    if request.user.is_authenticated():
        is_enrollment_admin = event.enrollment_event_meta.is_user_admin(request.user)

        try:
            person = request.user.person
            enrollment = Enrollment.objects.get(event=event, person=person)
        except (Person.DoesNotExist, Enrollment.DoesNotExist):
            pass

    return dict(
        enrollment=enrollment,
        is_enrollment_admin=is_enrollment_admin,
    )
