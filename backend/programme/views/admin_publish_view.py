from django.utils.translation import gettext_lazy as _

from labour.views.admin_startstop_view import generic_publish_unpublish_view

from ..forms import PublishForm
from ..helpers import programme_admin_required


@programme_admin_required
def admin_publish_view(request, vars, event):
    return generic_publish_unpublish_view(
        request,
        vars,
        event,
        meta=event.programme_event_meta,
        template="programme_admin_publish_view.pug",
        FormClass=PublishForm,
        save_success_message=_("The publication time was saved."),
        start_now_success_message=_("The schedule was published."),
        stop_now_success_message=_("The schedule was un-published."),
        already_public_message=_("The schedule was already public."),
    )
