from __future__ import annotations

from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import ClassVar, Self

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


class Column(pydantic.BaseModel):
    slug: str
    title: dict[str, str]
    type: TypeOfColumn


class Report(pydantic.BaseModel):
    slug: str
    title: dict[str, str]

    columns: list[Column]
    rows: list[list[Value]]

    @classmethod
    def from_query(
        cls,
        *,
        slug: str,
        title: dict[str, str],
        columns: list[Column],
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
        "total",
    ]
    row_titles: ClassVar[dict[str, dict[str, str]]] = dict(
        new=dict(
            fi="Uusi",
            en="New",
        ),
        fail=dict(
            fi="Epäonnistunut",
            en="Failed",
        ),
        ok_after_fail=dict(
            fi="OK epäonnistuneiden yritysten jälkeen",
            en="OK after failed attempts",
        ),
        ok_without_fail=dict(
            fi="OK ilman epäonnistuneita yrityksiä",
            en="OK without failed attempts",
        ),
        total=dict(
            fi="Yhteensä",
            en="Total",
        ),
    )

    @cached_property
    def total(self):
        return self.new + self.fail + self.ok_after_fail + self.ok_without_fail

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
        )


def payment_attempts_by_payment_method(
    event: Event,
    lang: str = DEFAULT_LANGUAGE,
) -> Report:
    return Report.from_query(
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
                slug="total",
                title=dict(
                    en="Total",
                    fi="Yhteensä",
                ),
                type=TypeOfColumn.INT,
            ),
        ],
    )


def get_reports(event: Event, lang: str = DEFAULT_LANGUAGE) -> list[Report]:
    return [
        OrdersByPaymentStatus.for_event(event).to_report(lang),
        payment_attempts_by_payment_method(event, lang),
    ]
