"""
Generic table report facility to avoid having to build markup for each report separately.
Also handles stuff like totals, formatting, and so on.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from django.db import connection

from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.report import Column, Report

SQL_DIR = Path(__file__).parent / "sql"


def report_from_query(
    *,
    query_args: list[Any] | dict[str, Any] | None = None,
    slug: str,
    title: dict[str, str],
    columns: list[Column],
    has_total_row: bool = False,
    lang: str = DEFAULT_LANGUAGE,
    footer: dict[str, str] | None = None,
) -> Report:
    query = (SQL_DIR / f"report_{slug}.sql").read_text()

    with connection.cursor() as cursor:
        cursor.execute(query, query_args)
        rows = cursor.fetchall()

    return Report(
        slug=slug,
        title=title,
        columns=columns,
        rows=rows,
        has_total_row=has_total_row,
        lang=lang,
        footer=footer,
    )
