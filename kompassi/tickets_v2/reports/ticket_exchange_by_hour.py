from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import ClassVar, Self

import pydantic
from django.db import connection

from kompassi.core.models.event import Event
from kompassi.core.utils.locale_utils import get_message_in_language
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.report import Column, Report, TypeOfColumn

SQL_DIR = Path(__file__).parent / "sql"


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
