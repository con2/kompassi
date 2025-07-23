from django.utils.translation import gettext_lazy as _

from kompassi.labour.views.admin_startstop_view import generic_publish_unpublish_view

from ..forms import EnrollmentStartForm
from ..helpers import enrollment_admin_required


@enrollment_admin_required
def enrollment_admin_start_view(request, vars, event):
    return generic_publish_unpublish_view(
        request,
        vars,
        event,
        meta=event.enrollment_event_meta,
        template="enrollment_admin_start_view.pug",
        FormClass=EnrollmentStartForm,
        save_success_message=_("The times for the enrollment period were saved."),
        start_now_success_message=_("The enrollment period was started."),
        stop_now_success_message=_("The enrollment period was ended."),
        already_public_message=_("The event was already accepting enrollments."),
    )
