from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from paikkala.models.tickets import Ticket as PaikkalaTicket

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models import Event
from kompassi.event_log_v2.utils.emit import emit
from kompassi.program_v2.models.schedule_item import ScheduleItem

from ..excel_export import write_reservations_as_excel


def paikkala_admin_export_view(
    request: HttpRequest,
    event_slug: str,
    schedule_item_slug: str,
):
    timestamp = now().strftime("%Y%m%d%H%M%S")
    event = get_object_or_404(Event, slug=event_slug)
    filename = f"{event.slug}_reservations_{timestamp}.xlsx"

    meta = event.program_v2_event_meta
    if meta is None:
        return HttpResponseBadRequest("Event does not use Program V2.")

    schedule_item = get_object_or_404(ScheduleItem, program__event=event, slug=schedule_item_slug)

    # TODO(#324): Failed check causes 500 now, turn it to 403 (middleware?)
    graphql_check_instance(
        schedule_item,
        request,
        app="program_v2",
        field="reservations",
        operation="query",
    )

    reservations = PaikkalaTicket.objects.filter(program__kompassi_v2_schedule_item=schedule_item).order_by(
        "zone",
        "row",
        "number",
    )

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    emit("core.person.exported", request=request)

    write_reservations_as_excel(
        reservations,
        response,
    )

    return response
