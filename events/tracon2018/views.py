from django.utils.timezone import now

from core.csv_export import csv_response
from labour.helpers import labour_admin_required

from .proxies import SignupExtraAfterpartyProxy


@labour_admin_required
def tracon2018_afterparty_participants_view(request, vars, event):
    assert event.slug == 'tracon2018'

    participants = SignupExtraAfterpartyProxy.objects.filter(afterparty_participation=True)

    filename = "{event.slug}_afterparty_participants_{timestamp}.xlsx".format(
        event=event,
        timestamp=now().strftime('%Y%m%d%H%M%S'),
        format=format,
    )

    return csv_response(event, SignupExtraAfterpartyProxy, participants,
        dialect='xlsx',
        filename=filename,
        m2m_mode='separate_columns',
    )
