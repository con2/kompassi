from django.shortcuts import render

from ..helpers import programme_admin_required
from ..models import Programme


@programme_admin_required
def admin_reservation_status_view(request, vars, event):
    programmes_with_reservation_status = []

    for programme in Programme.objects.filter(category__event=event, is_using_paikkala=True):
        baikal = programme.paikkala_program
        zones = []
        programme_reservation_status = dict(total_reserved=0, total_remaining=0, total_capacity=0)
        for zone in baikal.zones.all():
            zone_reservation_status = zone.get_reservation_status(baikal)
            programme_reservation_status["total_reserved"] += zone_reservation_status.total_reserved
            programme_reservation_status["total_remaining"] += zone_reservation_status.total_remaining
            programme_reservation_status["total_capacity"] += zone_reservation_status.total_capacity
            zones.append((zone, zone_reservation_status))

        programmes_with_reservation_status.append((programme, zones, programme_reservation_status))

    vars.update(
        programmes_with_reservation_status=programmes_with_reservation_status,
    )

    return render(request, "programme_admin_reservation_status_view.pug", vars)
