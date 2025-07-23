from django.shortcuts import render

from kompassi.badges.models.badge import Badge

from ..helpers import badges_admin_required


@badges_admin_required
def badges_admin_reports_view(request, vars, event):
    vars.update(
        arrivals_by_hour=Badge.get_arrivals_by_hour(event),
    )

    return render(request, "badges_admin_reports_view.pug", vars)
