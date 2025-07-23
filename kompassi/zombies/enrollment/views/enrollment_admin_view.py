from django.shortcuts import render

from kompassi.core.sort_and_filter import Filter

from ..helpers import enrollment_admin_required
from ..models.enrollment import STATE_CHOICES, Enrollment


@enrollment_admin_required
def enrollment_admin_view(request, vars, event):
    enrollments = (
        Enrollment.objects.filter(event=event)
        .select_related("person")
        .order_by("person__surname", "person__first_name")
    )

    state_filters = Filter(request, "state").add_choices("state", STATE_CHOICES)
    enrollments = state_filters.filter_queryset(enrollments)

    vars.update(
        enrollments=enrollments,
        num_enrolled=enrollments.count(),
        num_total_enrolled=enrollments.count(),
        state_filters=state_filters,
    )

    return render(request, "enrollment_admin_view.pug", vars)
