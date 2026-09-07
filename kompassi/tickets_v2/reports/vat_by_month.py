from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from django.db import connection

from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.column import Column
from kompassi.reports.models.enums import TotalBy, TypeOfColumn
from kompassi.reports.models.report import Report

from ..optimized_server.utils.formatting import format_vat_rate

SQL_DIR = Path(__file__).parent / "sql"

TITLE = dict(
    fi="ALV-erittely kuukausittain",
    en="VAT by month",
    sv="Moms per månad",
)
MONTH_COLUMN_TITLE = dict(fi="Kuukausi", en="Month", sv="Månad")
VAT_RATE_COLUMN_TITLE = dict(fi="ALV-kanta", en="VAT rate", sv="Momssats")
SOLD_COLUMN_TITLE = dict(fi="Myynti", en="Sold", sv="Försäljning")
RETURNED_COLUMN_TITLE = dict(fi="Palautukset", en="Returned", sv="Återbetalningar")
NET_COLUMN_TITLE = dict(fi="Netto", en="Net", sv="Netto")
VAT_COLUMN_TITLE = dict(fi="Maksettava vero", en="Tax payable", sv="Moms att betala")
FOOTER = dict(
    fi=(
        "Myynti kirjataan sille kuukaudelle, jona maksu on kirjattu, ja palautus sille "
        "kuukaudelle, jona hyvitys on kirjattu. Summat sisältävät arvonlisäveron. "
        "Maksettava vero on laskettu nettomyynnistä ja voi olla negatiivinen. Palautukset, "
        "jotka ovat vielä kesken maksupalveluntarjoajalla, eivät näy ennen kuin ne on vahvistettu."
    ),
    en=(
        "A sale is counted in the month the payment was recorded, and a return in the month "
        "the refund was recorded. Amounts include VAT. Tax payable is computed on net sales "
        "and can be negative. Refunds still pending at the payment provider are not counted "
        "until confirmed."
    ),
    sv=(
        "En försäljning räknas till den månad då betalningen registrerades, och en "
        "återbetalning till den månad då återbetalningen registrerades. Beloppen inkluderar "
        "moms. Moms att betala beräknas på nettoförsäljningen och kan vara negativ. "
        "Återbetalningar som fortfarande väntar hos betalningsleverantören räknas inte "
        "förrän de bekräftats."
    ),
)
CENT = Decimal("0.01")


class VatByMonth:
    query = (SQL_DIR / "report_vat_by_month.sql").read_text()

    @classmethod
    def report(cls, event: Event, lang: str = DEFAULT_LANGUAGE) -> Report:
        with connection.cursor() as cursor:
            cursor.execute(
                cls.query,
                dict(
                    event_id=event.id,
                    event_timezone=event.timezone_name,
                ),
            )
            raw_rows = cursor.fetchall()

        columns: list[Column] = [
            Column(
                slug="month",
                title=MONTH_COLUMN_TITLE,
                type=TypeOfColumn.STRING,
                # NOTE: total_by defaults to SUM, which is what makes the total
                # row label show "Total" in column 0 (see Report.get_total_row).
            ),
            Column(
                slug="vat_rate",
                title=VAT_RATE_COLUMN_TITLE,
                type=TypeOfColumn.STRING,
                total_by=TotalBy.NONE,
            ),
            Column(
                slug="sold",
                title=SOLD_COLUMN_TITLE,
                type=TypeOfColumn.CURRENCY,
            ),
            Column(
                slug="returned",
                title=RETURNED_COLUMN_TITLE,
                type=TypeOfColumn.CURRENCY,
            ),
            Column(
                slug="net",
                title=NET_COLUMN_TITLE,
                type=TypeOfColumn.CURRENCY,
            ),
            Column(
                slug="vat",
                title=VAT_COLUMN_TITLE,
                type=TypeOfColumn.CURRENCY,
            ),
        ]

        rows: list[list] = [
            [
                month,
                f"{format_vat_rate(vat_rate, lang)}%",
                float(sold.quantize(CENT)),
                float(returned.quantize(CENT)),
                float(net.quantize(CENT)),
                float(vat.quantize(CENT)),
            ]
            for month, vat_rate, sold, returned, net, vat in raw_rows
        ]

        return Report(
            slug="vat_by_month",
            title=TITLE,
            columns=columns,
            rows=rows,
            has_total_row=bool(rows),
            lang=lang,
            footer=FOOTER,
        )
