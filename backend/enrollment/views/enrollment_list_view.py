from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from ..helpers import enrollment_event_required
from ..models import Enrollment


@enrollment_event_required
def enrollment_list_view(request, event):
    meta = event.enrollment_event_meta

    if not meta.is_participant_list_public:
        if meta.is_user_admin(request.user):
            messages.warning(
                request,
                _(
                    "The participant list for this event is not public. "
                    "You are only seeing this page because you are an event admin."
                ),
            )
        else:
            messages.error(request, _("The participant list for this event is not public."))
            return redirect("core_event_view", event.slug)

    # TODO Order? Cannot order by ('person__surname', 'person__first_name') bc that would give away
    # information about possibly non-public fields.
    enrollments = Enrollment.objects.filter(event=event, state="ACCEPTED", is_public=True)

    return render(
        request,
        "enrollment_list_view.pug",
        dict(
            event=event,
            enrollments=enrollments,
            num_enrollments=enrollments.count(),
            num_total_enrollments=Enrollment.objects.filter(event=event, state="ACCEPTED").count(),
        ),
    )
