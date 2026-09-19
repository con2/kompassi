from decimal import Decimal

from django.db.models import F, Sum
from django.shortcuts import render
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.http import require_safe
from lippukala.consts import USED
from lippukala.models import Code
from paikkala.models import Ticket

from kompassi.core.models import Event
from kompassi.dimensions.models.enums import DimensionApp
from kompassi.forms.models.enums import SurveyPurpose
from kompassi.forms.models.response import Response
from kompassi.labour.models import ArchivedSignup, Signup
from kompassi.tickets_v2.models.order import Order as OrderV2
from kompassi.tickets_v2.optimized_server.models.enums import PaymentStatus
from kompassi.tickets_v2.optimized_server.utils.formatting import format_money
from kompassi.zombies.programme.models.programme import PROGRAMME_STATES_LIVE, Programme
from kompassi.zombies.tickets.models import Order, OrderProduct


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

    program_offers_v2 = Response.objects.filter(
        form__survey__app=DimensionApp.PROGRAM,
        form__survey__purpose=SurveyPurpose.DEFAULT,
        superseded_by=None,
    )
    paid_orders_v2 = OrderV2.objects.filter(cached_status=PaymentStatus.PAID)

    program_count_v1 = Programme.objects.count()
    program_count_v2 = program_offers_v2.count()
    accepted_program_count_v1 = Programme.objects.filter(state__in=PROGRAMME_STATES_LIVE).count()
    accepted_program_count_v2 = program_offers_v2.filter(cached_dimensions__state=["accepted"]).count()
    paid_order_count_v1 = Order.objects.filter(
        confirm_time__isnull=False,
        payment_date__isnull=False,
        cancellation_time__isnull=True,
    ).count()
    paid_order_count_v2 = paid_orders_v2.count()

    revenue_v1 = Decimal(revenue or 0) / 100
    revenue_v2 = paid_orders_v2.aggregate(revenue=Sum("cached_price"))["revenue"] or Decimal(0)

    vars = dict(
        events_count=Event.objects.count(),
        program_count_v1=program_count_v1,
        program_count_v2=program_count_v2,
        program_count_total=program_count_v1 + program_count_v2,
        accepted_program_count_v1=accepted_program_count_v1,
        accepted_program_count_v2=accepted_program_count_v2,
        accepted_program_count_total=accepted_program_count_v1 + accepted_program_count_v2,
        signup_count=signup_count,
        accepted_signup_count=accepted_signup_count,
        confirmed_order_count=Order.objects.filter(confirm_time__isnull=False).count(),
        paid_order_count_v1=paid_order_count_v1,
        paid_order_count_v2=paid_order_count_v2,
        paid_order_count_total=paid_order_count_v1 + paid_order_count_v2,
        etickets_issued=Code.objects.count(),
        etickets_used=Code.objects.filter(status=USED).count(),
        seat_reservations_issued=Ticket.objects.count(),
        formatted_revenue_v1=format_money(revenue_v1),
        formatted_revenue_v2=format_money(revenue_v2),
        formatted_revenue_total=format_money(revenue_v1 + revenue_v2),
        login_page=True,  # cached -> do not show other user's name in the header
    )

    return render(request, "core_stats_view.pug", vars)
