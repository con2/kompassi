# encodig: utf-8



from django.shortcuts import render

from ..helpers import enrollment_admin_required
from ..models import Enrollment


@enrollment_admin_required
def enrollment_admin_view(request, vars, event):
    enrollments = (
        Enrollment.objects.filter(event=event)
            .select_related('person')
            .order_by('person__surname', 'person__first_name')
    )

    vars.update(
        enrollments=enrollments,
        num_enrolled=enrollments.count(),
        num_total_enrolled=enrollments.count(),
    )

    return render(request, 'enrollment_admin_view.jade', vars)
