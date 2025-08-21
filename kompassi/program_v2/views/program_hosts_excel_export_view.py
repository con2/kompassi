from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models import Event
from kompassi.dimensions.filters import DimensionFilters
from kompassi.event_log_v2.utils.emit import emit
from kompassi.program_v2.graphql.program_host_full import ProgramHost

from ..excel_export import write_program_hosts_as_excel


def program_hosts_excel_export_view(
    request: HttpRequest,
    event_slug: str | None,
):
    timestamp = now().strftime("%Y%m%d%H%M%S")
    # TODO survey.scope instead of survey.event
    event = get_object_or_404(Event, slug=event_slug)
    filename = f"{event.slug}_program-hosts_{timestamp}.xlsx"

    meta = event.program_v2_event_meta
    if meta is None:
        return HttpResponseBadRequest("Event does not use Program V2.")

    # TODO(#324): Failed check causes 500 now, turn it to 403 (middleware?)
    graphql_check_instance(
        event,  # type: ignore
        request,
        app="program_v2",
        field="program_offers",
        operation="query",
    )

    emit("core.person.exported", request=request)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    hosts = ProgramHost.from_event(
        meta,
        program_filters=DimensionFilters.from_query_dict(request.GET),
        # involvement_filters=DimensionFilters.from_graphql(involvement_filters),  # TODO
    )

    write_program_hosts_as_excel(
        hosts,
        response,
    )

    return response
