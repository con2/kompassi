from __future__ import annotations

from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.report import TOTAL, Column, TypeOfColumn

from .report_from_query import report_from_query


def ticket_exchange_by_product(
    event: Event,
    lang: str = DEFAULT_LANGUAGE,
):
    return report_from_query(
        slug="ticket_exchange_by_product",
        title=dict(
            en="Ticket exchange by product",
            fi="Lippujen lunastus tuotteittain",
        ),
        query_args=dict(event_slug=event.slug),
        columns=[
            Column(
                slug="product",
                title=dict(
                    en="Product",
                    fi="Tuote",
                ),
                type=TypeOfColumn.STRING,
            ),
            Column(
                slug="not_exchanged",
                title=dict(
                    en="Not exchanged",
                    fi="Ei lunastettu",
                ),
                type=TypeOfColumn.INT,
            ),
            Column(
                slug="exchanged",
                title=dict(
                    en="Exchanged",
                    fi="Lunastettu",
                ),
                type=TypeOfColumn.INT,
            ),
            Column(
                slug="total",
                title=TOTAL,
                type=TypeOfColumn.INT,
            ),
        ],
        has_total_row=True,
        lang=lang,
    )
