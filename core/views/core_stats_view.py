from django.db.models import F, Sum
from django.shortcuts import render
from django.views.decorators.cache import cache_page, cache_control
from django.views.decorators.http import require_safe

from core.models import Event
from programme.models.programme import Programme, PROGRAMME_STATES_LIVE
from labour.models import Signup
from tickets.models import Order, OrderProduct
from tickets.utils import format_price
from lippukala.models import Code
from lippukala.consts import USED
from paikkala.models import Ticket


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

    vars = dict(
        events_count=Event.objects.count(),
        program_count=Programme.objects.count(),
        accepted_program_count=Programme.objects.filter(state__in=PROGRAMME_STATES_LIVE).count(),
        signup_count=Signup.objects.count(),
        accepted_signup_count=Signup.objects.filter(time_accepted__isnull=False).count(),
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
    )

    return render(request, "core_stats_view.pug", vars)
