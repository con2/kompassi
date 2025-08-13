from __future__ import annotations

import json
from pathlib import Path

from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.report import Column, Report, TypeOfColumn
from kompassi.tickets_v2.models.order import PaymentProvider

from .report_from_query import report_from_query

SQL_DIR = Path(__file__).parent / "sql"


def sales_by_payment_provider(
    event: Event,
    lang: str = DEFAULT_LANGUAGE,
) -> Report:
    return report_from_query(
        slug="sales_by_payment_provider",
        title=dict(
            en="Sales by payment provider",
            fi="Myynti maksunvälittäjittäin",
        ),
        query_args=dict(
            payment_providers=json.dumps([{"id": pm.value, "title": pm.name} for pm in PaymentProvider]),
            event_id=event.id,
        ),
        columns=[
            Column(
                slug="payment_provider",
                title=dict(
                    en="Payment provider",
                    fi="Maksutapa",
                ),
                type=TypeOfColumn.STRING,
            ),
            Column(
                slug="total_sold",
                title=dict(
                    en="Total sold",
                    fi="Myyty",
                ),
                type=TypeOfColumn.CURRENCY,
            ),
            Column(
                slug="total_paid",
                title=dict(
                    en="Total paid",
                    fi="Maksettu",
                ),
                type=TypeOfColumn.CURRENCY,
            ),
        ],
        has_total_row=True,
        lang=lang,
        footer=dict(
            en="Total cancelled is not included in total sold or total paid.",
            fi="Perutut tilaukset eivät sisälly myytyihin tai maksettuihin.",
        ),
    )
