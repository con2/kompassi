from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.http import require_safe

from ..helpers import programme_event_required


@programme_event_required
@require_safe
def schedule_redirect_view(
    request,
    event,
):
    meta = event.program_v2_event_meta
    if meta is None:
        raise Http404("Event does not have program v2 data")

    return redirect(meta.schedule_url)
