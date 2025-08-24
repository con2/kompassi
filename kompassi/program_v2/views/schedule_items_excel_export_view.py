from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models import Event
from kompassi.program_v2.filters import ProgramFilters

from ..excel_export import write_schedule_items_as_excel


def schedule_items_excel_export_view(
    request: HttpRequest,
    event_slug: str | None,
):
    timestamp = now().strftime("%Y%m%d%H%M%S")
    event = get_object_or_404(Event, slug=event_slug)
    filename = f"{event.slug}_schedule-items_{timestamp}.xlsx"

    meta = event.program_v2_event_meta
    if meta is None:
        return HttpResponseBadRequest("Event does not use Program V2.")

    # TODO(#324): Failed check causes 500 now, turn it to 403 (middleware?)
    graphql_check_instance(
        event,  # type: ignore
        request,
        app="program_v2",
        field="schedule_items",
        operation="query",
    )

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    schedule_items = ProgramFilters.from_query_dict(request.GET).filter_schedule_items(meta.schedule_items)
    dimensions = meta.universe.dimensions.filter(is_key_dimension=True).order_by("order")

    write_schedule_items_as_excel(
        event,
        schedule_items,
        response,
        dimensions,
    )

    return response
