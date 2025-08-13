from __future__ import annotations

from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.report import TOTAL, Column, Report, TotalBy, TypeOfColumn

from .report_from_query import report_from_query


def payment_attempts_by_payment_method(
    event: Event,
    lang: str = DEFAULT_LANGUAGE,
) -> Report:
    report = report_from_query(
        slug="payment_attempts_by_payment_method",
        title=dict(
            en="Payment attempts by payment method",
            fi="Maksuyritykset maksutavoittain",
        ),
        query_args=dict(event_id=event.id),
        columns=[
            Column(
                slug="payment_method",
                title=dict(
                    en="Payment method",
                    fi="Maksutapa",
                ),
                type=TypeOfColumn.STRING,
            ),
            Column(
                slug="ok",
                title=dict(
                    en="OK",
                    fi="OK",
                ),
                type=TypeOfColumn.INT,
            ),
            Column(
                slug="failed",
                title=dict(
                    en="Failed",
                    fi="Epäonnistuneet",
                ),
                type=TypeOfColumn.INT,
            ),
            Column(
                slug="failed_ratio",
                title=dict(
                    en="Failed ratio",
                    fi="Epäonnistuneiden osuus",
                ),
                type=TypeOfColumn.PERCENTAGE,
                total_by=TotalBy.NONE,
            ),
            Column(
                slug="total",
                title=TOTAL,
                type=TypeOfColumn.INT,
            ),
        ],
        has_total_row=True,
        footer=dict(
            en="Only showing payments done via Paytrail.",
            fi="Näytetään vain Paytrailin kautta tehdyt maksut.",
        ),
        lang=lang,
    )

    # HACK failed_ratio = failed / total is an intra-row calculation that doesn't add up to 1.0 column-wise
    # so total_by=TotalBy.AVERAGE is insufficient
    if report.total_row is None:
        raise AssertionError("No it isn't (appease typechecker)")
    failed_index, failed_ratio_index, total_index = (
        next(ind for (ind, col) in enumerate(report.columns) if col.slug == slug)
        for slug in ("failed", "failed_ratio", "total")
    )
    if (
        isinstance((total := report.total_row[total_index]), (int, float))
        and total > 0
        and isinstance((failed := report.total_row[failed_index]), (int, float))
    ):
        report.total_row[failed_ratio_index] = failed / total

    return report
