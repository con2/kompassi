from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from core.utils import initialize_form
from paikkala.models import Ticket


@login_required
def programme_profile_reservations_view(request):
    valid_tickets = Ticket.objects.valid().filter(user=request.user)
    past_tickets = Ticket.objects.filter(user=request.user).exclude(id__in=valid_tickets)

    vars = dict(
        valid_tickets=valid_tickets,
        past_tickets=past_tickets,
    )

    return render(request, 'programme_profile_reservations_view.pug', vars)
