from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from lippukala.consts import BEYOND_LOGIC, MANUAL_INTERVENTION_REQUIRED
from lippukala.views import POSView

from kompassi.access.cbac import default_cbac_required
from kompassi.core.models.event import Event


class TicketsV2POSView(POSView):
    def get_valid_codes(self, request):
        # Kompassi uses the MIR state for cancelled orders.
        return super().get_valid_codes(request).exclude(status__in=(MANUAL_INTERVENTION_REQUIRED, BEYOND_LOGIC))


_view = TicketsV2POSView.as_view()


@csrf_exempt
@default_cbac_required
def pos_view(request: HttpRequest, event_slug: str):
    event = get_object_or_404(Event, slug=event_slug)
    # XXX kala expects event filter via &event=foo; we specify it via /events/foo
    request.GET = request.GET.copy()
    request.GET["event"] = event.slug

    meta = event.tickets_v2_event_meta
    if not meta:
        messages.error(request, "Tämä tapahtuma ei käytä Kompassia lipunmyyntiin.")
        return redirect("core_event_view", event.slug)

    return _view(request)
