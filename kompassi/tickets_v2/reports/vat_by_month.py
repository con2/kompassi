from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from django.db import connection

from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.column import Column
from kompassi.reports.models.enums import TotalBy, TypeOfColumn
from kompassi.reports.models.report import Report

SQL_DIR = Path(__file__).parent / "sql"


def _format_vat_rate(rate: Decimal) -> dict[str, str]:
    normalized = rate.normalize()
    en = f"{normalized}%"
    fi = f"{str(normalized).replace('.', ',')}%"
    return dict(fi=fi, en=en)


class VatByMonth:
    query = (SQL_DIR / "report_vat_by_month.sql").read_text()

    @classmethod
    def report(cls, event: Event, lang: str = DEFAULT_LANGUAGE) -> Report:
        with connection.cursor() as cursor:
            cursor.execute(cls.query, dict(event_id=event.id, event_timezone=event.timezone_name))
            raw_rows = cursor.fetchall()

        if not raw_rows:
            return Report(
                slug="vat_by_month",
                title=dict(fi="ALV-erittely kuukausittain", en="VAT by month"),
                columns=[
                    Column(
                        slug="month",
                        title=dict(fi="Kuukausi", en="Month"),
                        type=TypeOfColumn.STRING,
                        total_by=TotalBy.NONE,
                    )
                ],
                rows=[],
                lang=lang,
            )

        months: list[str] = sorted({row[0] for row in raw_rows})
        vat_rates: list[Decimal] = sorted({row[1] for row in raw_rows})
        data: dict[tuple[str, Decimal], Decimal] = {(row[0], row[1]): row[2] for row in raw_rows}

        columns: list[Column] = [
            Column(
                slug="month",
                title=dict(fi="Kuukausi", en="Month"),
                type=TypeOfColumn.STRING,
                total_by=TotalBy.NONE,
            ),
            *[
                Column(
                    slug=f"vat_{rate}",
                    title=_format_vat_rate(rate),
                    type=TypeOfColumn.CURRENCY,
                )
                for rate in vat_rates
            ],
            Column(
                slug="total",
                title=dict(fi="Yhteensä", en="Total"),
                type=TypeOfColumn.CURRENCY,
            ),
        ]

        rows: list[list] = []
        for month in months:
            row_total = Decimal(0)
            row: list = [month]
            for rate in vat_rates:
                gross = data.get((month, rate), Decimal(0))
                row.append(float(gross))
                row_total += gross
            row.append(float(row_total))
            rows.append(row)

        return Report(
            slug="vat_by_month",
            title=dict(fi="ALV-erittely kuukausittain", en="VAT by month"),
            columns=columns,
            rows=rows,
            has_total_row=True,
            lang=lang,
            footer=dict(
                fi="Vain maksetut tilaukset on laskettu mukaan. Hyvitykset eivät sisälly raporttiin.",
                en="Only paid orders are included. Refunds are not reflected in this report.",
            ),
        )
