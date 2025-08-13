from __future__ import annotations

from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.report import Report

from .orders_by_payment_status import OrdersByPaymentStatus
from .payment_attempts_by_payment_method import payment_attempts_by_payment_method
from .sales_by_payment_provider import sales_by_payment_provider
from .ticket_exchange_by_hour import TicketExchangeByHour
from .ticket_exchange_by_product import ticket_exchange_by_product

REPORTS = dict(
    orders_by_payment_status=OrdersByPaymentStatus.report,
    payment_attempts_by_payment_method=payment_attempts_by_payment_method,
    sales_by_payment_provider=sales_by_payment_provider,
    ticket_exchange_by_product=ticket_exchange_by_product,
    ticket_exchange_by_hour=TicketExchangeByHour.report,
)


def get_reports(event: Event, lang: str = DEFAULT_LANGUAGE) -> list[Report]:
    return [report_func(event, lang) for report_func in REPORTS.values()]


def get_report(slug: str, event: Event, lang: str = DEFAULT_LANGUAGE) -> Report | None:
    return report_func(event, lang) if (report_func := REPORTS.get(slug)) else None
