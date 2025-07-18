"""
Generic table report facility to avoid having to build markup for each report separately.
Also handles stuff like totals, formatting, and so on.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Any, ClassVar, Self

import pydantic
from django.db import connection
from tabulate import tabulate

from core.models.event import Event
from core.utils.locale_utils import get_message_in_language
from graphql_api.language import DEFAULT_LANGUAGE

Value = int | float | str | None
SQL_DIR = Path(__file__).parent / "sql"


# named funnily to avoid ColumnType clash in GraphQL
class TypeOfColumn(Enum):
    INT = "int"
    STRING = "string"
    PERCENTAGE = "percentage"
    DATETIME = "datetime"


class TotalBy(Enum):
    NONE = "NONE"
    SUM = "SUM"
    AVERAGE = "AVERAGE"


class Column(pydantic.BaseModel):
    slug: str
    title: dict[str, str] = pydantic.Field(default_factory=dict)
    type: TypeOfColumn
    total_by: TotalBy = TotalBy.SUM

    def total_aggregate(self, values: list[Value]) -> Value:
        """
        We want to render the total row differently (tfoot > th).
        Additionally, producing it in SQL is usually a mess (UNION ALL etc).
        So produce it in Python.
        """
        if self.total_by == TotalBy.NONE:
            return ""

        numeric_values: list[int | float] = [value for value in values if isinstance(value, (int, float))]

        if not numeric_values:
            return ""

        match self.total_by:
            case TotalBy.SUM:
                return sum(numeric_values)
            case TotalBy.AVERAGE:
                return sum(numeric_values) / len(numeric_values)
            case _:
                raise NotImplementedError(self.total_by)


TOTAL = dict(
    fi="Yhteensä",
    en="Total",
)


class Report(pydantic.BaseModel):
    slug: str
    title: dict[str, str] = pydantic.Field(default_factory=dict)

    columns: list[Column]
    rows: list[list[Value]]
    total_row: list[Value] | None = None

    footer: dict[str, str] = pydantic.Field(default_factory=dict)

    lang: str = DEFAULT_LANGUAGE
    has_total_row: bool = False

    def get_total_row(self) -> list[Value]:
        total_row = []
        for col_ind, col in enumerate(self.columns):
            if col.total_by == TotalBy.NONE:
                total_row.append("")
                continue

            if col.type in (TypeOfColumn.INT, TypeOfColumn.PERCENTAGE):
                total_row.append(col.total_aggregate([row[col_ind] for row in self.rows]))
            elif col.type in (TypeOfColumn.STRING, TypeOfColumn.DATETIME):
                total_row.append(get_message_in_language(TOTAL, self.lang) if col_ind == 0 else "")
            else:
                raise NotImplementedError(col.type)
        return total_row

    def model_post_init(self, context: Any) -> None:
        if self.has_total_row:
            self.total_row = self.get_total_row()

    @classmethod
    def from_query(
        cls,
        *,
        slug: str,
        title: dict[str, str],
        columns: list[Column],
        has_total_row: bool = False,
        lang: str = DEFAULT_LANGUAGE,
        **kwargs,
    ) -> Report:
        query = (SQL_DIR / f"report_{slug}.sql").read_text()

        with connection.cursor() as cursor:
            cursor.execute(query, kwargs)
            rows = cursor.fetchall()

        return cls(
            slug=slug,
            title=title,
            columns=columns,
            rows=rows,
            has_total_row=has_total_row,
            lang=lang,
        )

    def print_tabular(self, lang: str = DEFAULT_LANGUAGE):
        print(
            tabulate(
                self.rows,
                headers=[get_message_in_language(col.title, lang) or col.slug for col in self.columns],
                stralign="left",
                numalign="right",
            )
        )


class OrdersByPaymentStatus(pydantic.BaseModel):
    new: int
    fail: int
    ok_after_fail: int
    ok_without_fail: int

    query: ClassVar[str] = (SQL_DIR / "report_orders_by_payment_status.sql").read_text()
    row_slugs: ClassVar[list[str]] = [
        "new",
        "fail",
        "ok_after_fail",
        "ok_without_fail",
    ]
    row_titles: ClassVar[dict[str, dict[str, str]]] = dict(
        new=dict(
            fi="Maksamista ei ole yritetty",
            en="Payment not attempted",
        ),
        fail=dict(
            fi="Maksaminen epäonnistui",
            en="Payment failed",
        ),
        ok_after_fail=dict(
            fi="Maksaminen onnistui epäonnistuneiden yritysten jälkeen",
            en="Payment succeeded after failed attempts",
        ),
        ok_without_fail=dict(
            fi="Maksaminen onnistui ensimmäisellä yrityksellä",
            en="Payment succeeded on first attempt",
        ),
    )

    @cached_property
    def total(self):
        return self.new + self.fail + self.ok_after_fail + self.ok_without_fail

    @classmethod
    def report(cls, event: Event, lang: str = DEFAULT_LANGUAGE) -> Report:
        return cls.for_event(event).to_report(lang)

    @classmethod
    def for_event(cls, event: Event) -> Self:
        with connection.cursor() as cursor:
            cursor.execute(cls.query, {"event_id": event.id})
            row = cursor.fetchone()

        if not row:
            return cls(new=0, fail=0, ok_after_fail=0, ok_without_fail=0)

        new, fail, ok_after_fail, ok_without_fail = row

        return cls(
            new=new,
            fail=fail,
            ok_after_fail=ok_after_fail,
            ok_without_fail=ok_without_fail,
        )

    def to_report(self, lang: str = DEFAULT_LANGUAGE) -> Report:
        return Report(
            slug="orders_by_payment_status",
            title=dict(
                fi="Tilausten maksutilanne",
                en="Orders by payment status",
            ),
            footer=dict(
                fi="Tilaukset, jotka on sittemmin peruttu, on laskettu mukaan näihin tilastoihin.",
                en="Orders that have been cancelled later are included in these statistics.",
            ),
            columns=[
                Column(
                    slug="status",
                    title=dict(
                        fi="Maksun tila",
                        en="Payment status",
                    ),
                    type=TypeOfColumn.STRING,
                ),
                Column(
                    slug="num_orders",
                    title=dict(
                        fi="Tilausten määrä",
                        en="Number of orders",
                    ),
                    type=TypeOfColumn.INT,
                ),
                Column(
                    slug="percentage",
                    title=dict(
                        fi="Prosenttiosuus",
                        en="Percentage",
                    ),
                    type=TypeOfColumn.PERCENTAGE,
                ),
            ],
            rows=[
                [
                    get_message_in_language(self.row_titles[row_slug], lang),
                    getattr(self, row_slug),
                    getattr(self, row_slug) / self.total if self.total else None,
                ]
                for row_slug in self.row_slugs
            ],
            has_total_row=True,
            lang=lang,
        )


def payment_attempts_by_payment_method(
    event: Event,
    lang: str = DEFAULT_LANGUAGE,
) -> Report:
    report = Report.from_query(
        slug="payment_attempts_by_payment_method",
        title=dict(
            en="Payment attempts by payment method",
            fi="Maksuyritykset maksutavoittain",
        ),
        event_id=event.id,
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


def ticket_exchange_by_product(
    event: Event,
    lang: str = DEFAULT_LANGUAGE,
):
    return Report.from_query(
        slug="ticket_exchange_by_product",
        title=dict(
            en="Ticket exchange by product",
            fi="Lippujen lunastus tuotteittain",
        ),
        event_slug=event.slug,
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


class TicketExchangeByHour(pydantic.BaseModel):
    hour: datetime | None
    arrivals: int
    cum_arrivals: int

    query: ClassVar[str] = (SQL_DIR / "report_ticket_exchange_by_hour.sql").read_text()

    not_exchanged: ClassVar[dict[str, str]] = dict(
        fi="Ei lunastettu",
        en="Not exchanged",
    )

    @classmethod
    def for_event(cls, event: Event) -> list[Self]:
        with connection.cursor() as cursor:
            cursor.execute(cls.query, dict(event_slug=event.slug))
            return [cls.model_validate(dict(zip(cls.model_fields, row, strict=True))) for row in cursor.fetchall()]

    @classmethod
    def report(cls, event: Event, lang: str = DEFAULT_LANGUAGE) -> Report:
        rows = cls.for_event(event)
        tz = event.timezone
        return Report(
            slug="ticket_exchange_by_hour",
            title=dict(
                en="Exchanged tickets by hour",
                fi="Lippujen lunastus tunneittain",
            ),
            columns=[
                Column(
                    slug="hour",
                    title=dict(
                        en="Hour",
                        fi="Tunti",
                    ),
                    type=TypeOfColumn.DATETIME,
                ),
                Column(
                    slug="arrivals",
                    title=dict(
                        en="Exchanged tickets in this hour",
                        fi="Tunnilla lunastettu",
                    ),
                    type=TypeOfColumn.INT,
                ),
                Column(
                    slug="cum_arrivals",
                    title=dict(
                        en="Total exchanged tickets",
                        fi="Lunastettu yhteensä",
                    ),
                    type=TypeOfColumn.INT,
                ),
            ],
            rows=[
                [
                    row.hour.astimezone(tz).isoformat()
                    if row.hour
                    else get_message_in_language(cls.not_exchanged, lang),
                    row.arrivals,
                    row.cum_arrivals,
                ]
                for row in rows
            ],
        )


REPORTS = dict(
    orders_by_payment_status=OrdersByPaymentStatus.report,
    payment_attempts_by_payment_method=payment_attempts_by_payment_method,
    ticket_exchange_by_product=ticket_exchange_by_product,
    ticket_exchange_by_hour=TicketExchangeByHour.report,
)


def get_reports(event: Event, lang: str = DEFAULT_LANGUAGE) -> list[Report]:
    return [get_report(event, lang) for get_report in REPORTS.values()]


def get_report(slug: str, event: Event, lang: str = DEFAULT_LANGUAGE) -> Report | None:
    return get_report(event, lang) if (get_report := REPORTS.get(slug)) else None
