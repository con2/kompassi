from __future__ import annotations

from pathlib import Path
from typing import Any

import pydantic

from kompassi.core.utils.locale_utils import get_message_in_language
from kompassi.graphql_api.language import DEFAULT_LANGUAGE

from .column import Column
from .enums import TotalBy, TypeOfColumn, Value

SQL_DIR = Path(__file__).parent / "sql"

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

    footer: dict[str, str] | None = None

    lang: str = DEFAULT_LANGUAGE
    has_total_row: bool = False

    def get_total_row(self) -> list[Value]:
        total_row = []
        for col_ind, col in enumerate(self.columns):
            if col.total_by == TotalBy.NONE:
                total_row.append("")
                continue

            if col.type in (TypeOfColumn.INT, TypeOfColumn.PERCENTAGE, TypeOfColumn.CURRENCY):
                total_row.append(col.total_aggregate([row[col_ind] for row in self.rows]))
            elif col.type in (TypeOfColumn.STRING, TypeOfColumn.DATETIME):
                total_row.append(get_message_in_language(TOTAL, self.lang) if col_ind == 0 else "")
            else:
                raise NotImplementedError(col.type)
        return total_row

    def model_post_init(self, context: Any) -> None:
        if self.has_total_row:
            self.total_row = self.get_total_row()
        if not self.footer:
            self.footer = dict()
