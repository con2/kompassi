from django.db.models import F, Sum
from django.shortcuts import render
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.http import require_safe
from lippukala.consts import USED
from lippukala.models import Code
from paikkala.models import Ticket

from kompassi.core.models import Event
from kompassi.labour.models import ArchivedSignup, Signup
from kompassi.zombies.programme.models.programme import PROGRAMME_STATES_LIVE, Programme
from kompassi.zombies.tickets.models import Order, OrderProduct
from kompassi.zombies.tickets.utils import format_price


@require_safe
@cache_control(public=True, max_age=5 * 60)
@cache_page(5 * 60)
def core_stats_view(request):
    revenue = (
        OrderProduct.objects.filter(
            order__confirm_time__isnull=False,
            order__payment_date__isnull=False,
            order__cancellation_time__isnull=True,
        )
        .annotate(sum=F("product__price_cents") * F("count"))
        .aggregate(revenue=Sum("sum"))["revenue"]
    )

    signup_count = Signup.objects.count() + ArchivedSignup.objects.count()
    accepted_signup_count = Signup.objects.filter(time_accepted__isnull=False).count() + ArchivedSignup.objects.count()

    vars = dict(
        events_count=Event.objects.count(),
        program_count=Programme.objects.count(),
        accepted_program_count=Programme.objects.filter(state__in=PROGRAMME_STATES_LIVE).count(),
        signup_count=signup_count,
        accepted_signup_count=accepted_signup_count,
        confirmed_order_count=Order.objects.filter(confirm_time__isnull=False).count(),
        paid_order_count=Order.objects.filter(
            confirm_time__isnull=False,
            payment_date__isnull=False,
            cancellation_time__isnull=True,
        ).count(),
        etickets_issued=Code.objects.count(),
        etickets_used=Code.objects.filter(status=USED).count(),
        seat_reservations_issued=Ticket.objects.count(),
        formatted_revenue=format_price(revenue),
        login_page=True,  # cached -> do not show other user's name in the header
    )

    return render(request, "core_stats_view.pug", vars)
