from typing import Any

from csp.decorators import csp_update
from django.db.models import Q
from django.shortcuts import render
from django.utils.timezone import now

from membership.views import membership_organization_box_context
from payments.models.checkout_payment import CHECKOUT_PAYMENT_WALL_ORIGIN

from ..helpers import public_organization_required
from ..models import Event
from ..utils import groups_of_n


@public_organization_required
@csp_update({"form-action": [CHECKOUT_PAYMENT_WALL_ORIGIN]})  # type: ignore
def core_organization_view(request, organization):
    t = now()

    past_events = Event.objects.filter(organization=organization, public=True, end_time__lte=t).order_by("-start_time")
    current_events = Event.objects.filter(
        organization=organization, public=True, start_time__lte=t, end_time__gt=t
    ).order_by("-start_time")
    future_events = Event.objects.filter(
        Q(organization=organization, public=True) & (Q(start_time__gt=t) | Q(start_time__isnull=True))
    ).order_by("start_time")

    vars: dict[str, Any] = dict(
        organization=organization,
        past_events_rows=list(groups_of_n(past_events, 4)),
        current_events_rows=list(groups_of_n(current_events, 4)),
        future_events_rows=list(groups_of_n(future_events, 4)),
    )

    vars.update(membership_organization_box_context(request, organization))

    return render(request, "core_organization_view.pug", vars)
