from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from core.utils import initialize_form
from paikkala.models import Ticket

from ..models import Programme


@login_required
def profile_reservations_view(request):
    t = now()
    valid_tickets = Ticket.objects.valid().filter(user=request.user)
    past_tickets = Ticket.objects.filter(user=request.user).exclude(id__in=valid_tickets)
    reservable_programmes = Programme.objects.filter(
        paikkala_program__reservation_start__lte=t,
        paikkala_program__reservation_end__gt=t,
        is_paikkala_public=True,
    )

    vars = dict(
        valid_tickets=valid_tickets,
        past_tickets=past_tickets,
        reservable_programmes=reservable_programmes,
    )

    return render(request, 'programme_profile_reservations_view.pug', vars)
