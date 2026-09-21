from __future__ import annotations

from decimal import Decimal

from django.db.models import F, Sum
from lippukala.consts import USED
from lippukala.models import Code
from paikkala.models import Ticket

from kompassi.core.models import Event
from kompassi.core.utils.locale_utils import get_message_in_language
from kompassi.dimensions.models.enums import DimensionApp
from kompassi.forms.models.enums import SurveyPurpose
from kompassi.forms.models.response import Response
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.labour.models import ArchivedSignup, Signup
from kompassi.reports.models.report import Column, Report, TypeOfColumn
from kompassi.tickets_v2.models.order import Order as OrderV2
from kompassi.tickets_v2.optimized_server.models.enums import PaymentStatus
from kompassi.zombies.programme.models.programme import PROGRAMME_STATES_LIVE, Programme
from kompassi.zombies.tickets.models import Order, OrderProduct

CENT = Decimal("0.01")

COLUMN_TITLES = dict(
    metric=dict(en="Metric", fi="Tunnusluku"),
    v1=dict(en="V1", fi="V1"),
    v2=dict(en="V2", fi="V2"),
    total=dict(en="Total", fi="Yhteensä"),
)

ROW_TITLES = dict(
    events=dict(en="Events", fi="Tapahtumat"),
    program_offers=dict(en="Program offers", fi="Ohjelmatarjoukset"),
    accepted_program_offers=dict(en="Accepted program offers", fi="Hyväksytyt ohjelmatarjoukset"),
    volunteer_signups=dict(en="Volunteer signups", fi="Työvoimailmoittautumiset"),
    accepted_volunteer_signups=dict(en="Accepted volunteer signups", fi="Hyväksytyt työvoimailmoittautumiset"),
    confirmed_ticket_orders=dict(en="Confirmed ticket orders", fi="Vahvistetut lipputilaukset"),
    paid_ticket_orders=dict(en="Paid ticket orders", fi="Maksetut lipputilaukset"),
    etickets_issued=dict(en="E-tickets issued", fi="Myönnetyt sähköiset liput"),
    etickets_used=dict(en="E-tickets used", fi="Käytetyt sähköiset liput"),
    seat_reservations_issued=dict(en="Seat reservations issued", fi="Myönnetyt paikkavaraukset"),
)


def _counts_report(lang: str) -> Report:
    """
    Paikkala and lippukala tables are shared between V1 and V2 and old event data
    was never split out, so e-tickets and seat reservations cannot be attributed
    to a version and are only reported as a total.
    """
    signup_count = Signup.objects.count() + ArchivedSignup.objects.count()
    accepted_signup_count = Signup.objects.filter(time_accepted__isnull=False).count() + ArchivedSignup.objects.count()
    confirmed_order_count = Order.objects.filter(confirm_time__isnull=False).count()

    program_offers_v2 = Response.objects.filter(
        form__survey__app=DimensionApp.PROGRAM,
        form__survey__purpose=SurveyPurpose.DEFAULT,
        superseded_by=None,
    )
    program_count_v1 = Programme.objects.count()
    program_count_v2 = program_offers_v2.count()
    accepted_program_count_v1 = Programme.objects.filter(state__in=PROGRAMME_STATES_LIVE).count()
    accepted_program_count_v2 = program_offers_v2.filter(cached_dimensions__state=["accepted"]).count()

    paid_order_count_v1 = Order.objects.filter(
        confirm_time__isnull=False,
        payment_date__isnull=False,
        cancellation_time__isnull=True,
    ).count()
    paid_order_count_v2 = OrderV2.objects.filter(cached_status=PaymentStatus.PAID).count()

    def title(slug: str) -> str:
        return get_message_in_language(ROW_TITLES[slug], lang) or ""

    def split_row(slug: str, v1: int, v2: int) -> list:
        return [title(slug), v1, v2, v1 + v2]

    def total_only_row(slug: str, total: int) -> list:
        return [title(slug), "", "", total]

    return Report(
        slug="kompassi_stats_counts",
        title=dict(en="Kompassi statistics", fi="Kompassin tilastot"),
        columns=[
            Column(slug="metric", title=COLUMN_TITLES["metric"], type=TypeOfColumn.STRING),
            Column(slug="v1", title=COLUMN_TITLES["v1"], type=TypeOfColumn.INT),
            Column(slug="v2", title=COLUMN_TITLES["v2"], type=TypeOfColumn.INT),
            Column(slug="total", title=COLUMN_TITLES["total"], type=TypeOfColumn.INT),
        ],
        rows=[
            total_only_row("events", Event.objects.count()),
            split_row("program_offers", program_count_v1, program_count_v2),
            split_row("accepted_program_offers", accepted_program_count_v1, accepted_program_count_v2),
            total_only_row("volunteer_signups", signup_count),
            total_only_row("accepted_volunteer_signups", accepted_signup_count),
            total_only_row("confirmed_ticket_orders", confirmed_order_count),
            split_row("paid_ticket_orders", paid_order_count_v1, paid_order_count_v2),
            total_only_row("etickets_issued", Code.objects.count()),
            total_only_row("etickets_used", Code.objects.filter(status=USED).count()),
            total_only_row("seat_reservations_issued", Ticket.objects.count()),
        ],
        lang=lang,
    )


def _revenue_report(lang: str) -> Report:
    revenue_v1_cents = (
        OrderProduct.objects.filter(
            order__confirm_time__isnull=False,
            order__payment_date__isnull=False,
            order__cancellation_time__isnull=True,
        )
        .annotate(sum=F("product__price_cents") * F("count"))
        .aggregate(revenue=Sum("sum"))["revenue"]
    )
    revenue_v1 = Decimal(revenue_v1_cents or 0) / 100
    revenue_v2 = OrderV2.objects.filter(cached_status=PaymentStatus.PAID).aggregate(revenue=Sum("cached_price"))[
        "revenue"
    ] or Decimal(0)

    title = dict(en="Ticket sales revenue", fi="Lipputulot")

    return Report(
        slug="kompassi_stats_revenue",
        title=title,
        columns=[
            Column(slug="metric", title=COLUMN_TITLES["metric"], type=TypeOfColumn.STRING),
            Column(slug="v1", title=COLUMN_TITLES["v1"], type=TypeOfColumn.CURRENCY),
            Column(slug="v2", title=COLUMN_TITLES["v2"], type=TypeOfColumn.CURRENCY),
            Column(slug="total", title=COLUMN_TITLES["total"], type=TypeOfColumn.CURRENCY),
        ],
        rows=[
            [
                get_message_in_language(title, lang) or "",
                float(revenue_v1.quantize(CENT)),
                float(revenue_v2.quantize(CENT)),
                float((revenue_v1 + revenue_v2).quantize(CENT)),
            ]
        ],
        lang=lang,
    )


def kompassi_stats_reports(lang: str = DEFAULT_LANGUAGE) -> list[Report]:
    return [_counts_report(lang), _revenue_report(lang)]
