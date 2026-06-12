from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from django.db import connection

from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.column import Column
from kompassi.reports.models.enums import TypeOfColumn
from kompassi.reports.models.report import Report

from ..optimized_server.models.enums import PaymentStatus
from ..optimized_server.utils.formatting import format_vat_rate

SQL_DIR = Path(__file__).parent / "sql"

TITLE = dict(
    fi="ALV-erittely kuukausittain",
    en="VAT by month",
    sv="Moms per månad",
)
MONTH_COLUMN_TITLE = dict(fi="Kuukausi", en="Month", sv="Månad")
TOTAL_COLUMN_TITLE = dict(fi="Yhteensä", en="Total", sv="Totalt")
FOOTER = dict(
    fi=(
        "Vain maksetut tilaukset on laskettu mukaan. Hyvitetyt tilaukset näkyvät "
        "alkuperäisen myyntikuukauden kohdalla; hyvityksiä ei vähennetä."
    ),
    en=(
        "Only paid orders are included. Refunded orders are shown in the month of "
        "the original sale; refunds are not subtracted."
    ),
    sv=(
        "Endast betalda beställningar ingår. Återbetalda beställningar visas under "
        "den ursprungliga försäljningsmånaden; återbetalningar dras inte av."
    ),
)
CENT = Decimal("0.01")

# Orders in these statuses have been paid at some point. A later refund must not
# retroactively remove the sale from the month it was made in, as the VAT for
# that month may already have been filed.
EVER_PAID_STATUSES = [
    PaymentStatus.PAID,
    PaymentStatus.REFUND_REQUESTED,
    PaymentStatus.REFUND_FAILED,
    PaymentStatus.REFUNDED,
]


def _vat_column_title(rate: Decimal) -> dict[str, str]:
    return {lang: f"{format_vat_rate(rate, lang)}%" for lang in ("fi", "en", "sv")}


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
                    paid_statuses=[status.value for status in EVER_PAID_STATUSES],
                ),
            )
            raw_rows = cursor.fetchall()

        vat_rates: list[Decimal] = sorted({row[1] for row in raw_rows})
        months: list[str] = sorted({row[0] for row in raw_rows})
        data: dict[tuple[str, Decimal], Decimal] = {(row[0], row[1]): row[2] for row in raw_rows}

        columns: list[Column] = [
            Column(
                slug="month",
                title=MONTH_COLUMN_TITLE,
                type=TypeOfColumn.STRING,
                # NOTE: total_by defaults to SUM, which is what makes the total
                # row label show "Total" in column 0 (see Report.get_total_row).
            ),
            *(
                Column(
                    slug=f"vat_{rate}",
                    title=_vat_column_title(rate),
                    type=TypeOfColumn.CURRENCY,
                )
                for rate in vat_rates
            ),
            Column(
                slug="total",
                title=TOTAL_COLUMN_TITLE,
                type=TypeOfColumn.CURRENCY,
            ),
        ]

        rows: list[list] = []
        for month in months:
            row: list = [month]
            row_total = Decimal(0)
            for rate in vat_rates:
                vat = data.get((month, rate), Decimal(0)).quantize(CENT)
                row.append(float(vat))
                row_total += vat
            row.append(float(row_total))
            rows.append(row)

        return Report(
            slug="vat_by_month",
            title=TITLE,
            columns=columns,
            rows=rows,
            has_total_row=bool(rows),
            lang=lang,
            footer=FOOTER,
        )
