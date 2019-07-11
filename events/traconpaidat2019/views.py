from django.utils.timezone import now

from core.csv_export import csv_response
from event_log.utils import emit
from tickets.helpers import tickets_admin_required

from .models import CustomShirtProxy



@tickets_admin_required
def traconpaidat2019_custom_shirts_view(request, vars, event):
    assert event.slug == 'traconpaidat2019'

    shirts = CustomShirtProxy.objects.all()

    filename = "{event.slug}_nimikoidut_{timestamp}.xlsx".format(
        event=event,
        timestamp=now().strftime('%Y%m%d%H%M%S'),
        format=format,
    )

    emit('core.person.exported', request=request, event=event)

    return csv_response(event, CustomShirtProxy, shirts,
        dialect='xlsx',
        filename=filename,
        m2m_mode='separate_columns',
    )
