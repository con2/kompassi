from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from core.csv_export import csv_response
from event_log_v2.utils.emit import emit

from ..helpers import programme_admin_required
from ..models import Programme
from ..proxies.paikkala_ticket import PaikkalaTicketCsvExportProxy


@programme_admin_required
def admin_reservations_export_view(request, vars, event, programme_id):
    programme = get_object_or_404(Programme, id=int(programme_id))
    tickets = PaikkalaTicketCsvExportProxy.objects.filter(program__kompassi_programme=programme)
    timestamp = now().strftime("%Y%m%d%H%M%S")

    emit("core.person.exported", request=request)

    return csv_response(
        event,
        PaikkalaTicketCsvExportProxy,
        tickets,
        dialect="xlsx",
        filename=f"{event.slug}_reservations_{programme_id}_{timestamp}.xlsx",
        m2m_mode="separate_columns",
    )
