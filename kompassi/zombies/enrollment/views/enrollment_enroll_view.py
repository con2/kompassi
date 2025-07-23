from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from kompassi.core.helpers import person_required
from kompassi.core.utils import initialize_form

from ..helpers import enrollment_event_required
from ..models import Enrollment


@enrollment_event_required
@person_required
def enrollment_enroll_view(request, event):
    meta = event.enrollment_event_meta
    can_enroll = request.user.person.official_first_names or not meta.is_official_name_required

    if not meta.is_enrollment_open:
        if meta.is_user_admin(request.user):
            messages.warning(
                request,
                _(
                    "Enrollment for this event is not currently open. "
                    "You are only seeing this page because you are an event admin."
                ),
            )
        else:
            messages.error(request, _("Enrollment for this event is not currently open."))
            return redirect("core_event_view", event.slug)

    try:
        enrollment = Enrollment.objects.get(event=event, person=request.user.person)
        already_enrolled = enrollment.is_active
    except Enrollment.DoesNotExist:
        enrollment = Enrollment(event=event, person=request.user.person)
        already_enrolled = False

    if enrollment.state == "REJECTED":
        messages.error(
            request,
            _(
                "Your enrollment for this event has been rejected by the organizer. "
                "You cannot re-enroll by yourself. If you believe this is in error, "
                "please contact the organizer."
            ),
        )
        return redirect("core_event_view", event.slug)

    EnrollmentForm = meta.form_class
    form = initialize_form(EnrollmentForm, request, instance=enrollment)

    if request.method == "POST" and can_enroll:
        action = request.POST["action"]

        if action == "save-return":
            if form.is_valid():
                enrollment = form.save(commit=False)
                enrollment.event = event
                enrollment.person = request.user.person

                if not already_enrolled:
                    enrollment.state = meta.initial_state

                enrollment.save()
                form.save_m2m()

                messages.success(request, _("Thank you for enrolling."))
                return redirect("core_event_view", event.slug)
            else:
                messages.error(request, _("Please check the form."))
        elif action == "cancel-enrollment":
            if already_enrolled:
                enrollment.cancel()
                messages.success(request, _("Your enrollment has now been cancelled."))
                return redirect("core_event_view", event.slug)
            else:
                messages.error(request, _("One does not simply cancel an enrollment that has not yet been made."))

    return render(
        request,
        "enrollment_enroll_view.pug",
        dict(
            already_enrolled=already_enrolled,
            can_enroll=can_enroll,
            enrollment=enrollment,
            event=event,
            form=form,
        ),
    )
