from django.shortcuts import render

from kompassi.core.utils import groups_of_n

from ..models import Organization


def core_organizations_view(request):
    organizations = Organization.objects.filter(public=True)

    vars = dict(
        organizations_rows=groups_of_n(organizations, 4),
    )

    return render(request, "core_organizations_view.pug", vars)
