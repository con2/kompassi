from typing import Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from access.cbac import default_cbac_required
from core.models import Event

from ..models import EventForm, GlobalForm
from ..excel_export import write_responses_as_excel


@default_cbac_required
def forms_excel_export_view(request: HttpRequest, event_slug: Optional[str], form_slug: str):
    if event_slug:
        event = get_object_or_404(Event, slug=event_slug)
        form = get_object_or_404(EventForm, event=event, slug=form_slug)
    else:
        form = get_object_or_404(GlobalForm, slug=form_slug)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="forms.xlsx"'

    write_responses_as_excel(form, form.responses.all().only("form_data"), response)

    return response
