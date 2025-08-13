from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import ClassVar, Self

import pydantic
from django.db import connection

from kompassi.core.models.event import Event
from kompassi.core.utils.locale_utils import get_message_in_language
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.report import Column, Report, TypeOfColumn

SQL_DIR = Path(__file__).parent / "sql"


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
