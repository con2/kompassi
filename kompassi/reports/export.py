"""
Download a Report as CSV or Excel. The frontend links here from each report card.
"""

from __future__ import annotations

import csv
import io
from datetime import datetime, tzinfo
from decimal import Decimal, InvalidOperation
from typing import BinaryIO, Literal

import xlsxwriter
from django.utils.timezone import now

from kompassi.core.utils.locale_utils import get_message_in_language

from .models.column import Column
from .models.enums import TypeOfColumn, Value
from .models.report import Report

ExportFormat = Literal["csv", "xlsx"]

CONTENT_TYPES: dict[ExportFormat, str] = {
    "csv": "text/csv; charset=utf-8",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

# A spreadsheet may run a text cell that starts with one of these as a formula.
# Cf. https://owasp.org/www-community/attacks/CSV_Injection
FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")

# Excel limits sheet names to 31 characters, none of these
SHEET_NAME_FORBIDDEN = str.maketrans(dict.fromkeys("[]:*?/\\", " "))


def parse_datetime(value: Value) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        # eg. the "Not exchanged" row of ticket_exchange_by_hour
        return None


def parse_decimal(value: Value) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def format_filename_time(dt: datetime, tz: tzinfo) -> str:
    return dt.astimezone(tz).strftime("%Y-%m-%dT%H%M")


def get_filename(
    report: Report,
    prefix: str,
    tz: tzinfo,
    format: ExportFormat,
    exported_at: datetime | None = None,
) -> str:
    """
    Reports with a datetime column are named after the first and last time in it,
    eg. ropecon2026_ticket_exchange_by_hour_2026-07-24T1000_2026-07-26T1800.csv.
    Other reports cover everything up to the moment of export,
    eg. ropecon2026_ticket_exchange_by_product_until_2026-10-24T1530.csv.
    """
    datetime_column_index = next(
        (ind for ind, column in enumerate(report.columns) if column.type == TypeOfColumn.DATETIME),
        None,
    )
    datetimes = (
        sorted(dt for row in report.rows if (dt := parse_datetime(row[datetime_column_index])))
        if datetime_column_index is not None
        else []
    )

    if datetimes:
        time_range = f"{format_filename_time(datetimes[0], tz)}_{format_filename_time(datetimes[-1], tz)}"
    else:
        time_range = f"until_{format_filename_time(exported_at or now(), tz)}"

    return f"{prefix}_{report.slug}_{time_range}.{format}"


def neutralize_formula(text: str) -> str:
    return "'" + text if text.startswith(FORMULA_PREFIXES) else text


def get_column_title(column: Column, lang: str) -> str:
    # eg. dimension value titles are entered by admins and may be missing
    return get_message_in_language(column.title, lang) or column.slug


def get_sheet_name(report: Report, lang: str) -> str:
    title = get_message_in_language(report.title, lang) or ""
    # Excel also forbids an apostrophe at either end, which truncation may leave there,
    # and a name of only spaces, which is what a title of only forbidden characters becomes
    return title.translate(SHEET_NAME_FORBIDDEN)[:31].strip("' ") or report.slug[:31]


def write_csv(report: Report, lang: str, output_stream: BinaryIO):
    """
    Raw values rather than the formatted ones shown in the table, so that
    scripts and spreadsheets can treat numbers and times as such. The total row is
    left out so it does not get summed along with the data.
    """
    buf = io.StringIO()
    writer = csv.writer(buf)

    writer.writerow(neutralize_formula(get_column_title(column, lang)) for column in report.columns)
    for row in report.rows:
        writer.writerow(
            ""
            if value is None
            else neutralize_formula(value)
            if column.type == TypeOfColumn.STRING and isinstance(value, str)
            else value
            for column, value in zip(report.columns, row, strict=True)
        )

    # BOM so that Excel detects UTF-8 and shows ä and ö correctly
    output_stream.write(buf.getvalue().encode("utf-8-sig"))


def write_xlsx(report: Report, lang: str, tz: tzinfo, output_stream: BinaryIO):
    """
    Typed cells, so that Excel shows numbers, money, percentages and times correctly
    regardless of the regional settings of the computer. Excel does not support time
    zones, so times are written as local time of the event. As in the CSV, no total row.
    """
    buf = io.BytesIO()
    workbook = xlsxwriter.Workbook(buf, {"in_memory": True})

    worksheet = workbook.add_worksheet(get_sheet_name(report, lang))

    header_format = workbook.add_format({"bold": True})
    formats = {
        TypeOfColumn.CURRENCY: workbook.add_format({"num_format": "#,##0.00 €"}),
        TypeOfColumn.PERCENTAGE: workbook.add_format({"num_format": "0.0%"}),
        TypeOfColumn.DATETIME: workbook.add_format({"num_format": "yyyy-mm-dd hh:mm"}),
    }

    for col_ind, column in enumerate(report.columns):
        column_title = get_column_title(column, lang)
        worksheet.write_string(0, col_ind, column_title, header_format)
        worksheet.set_column(col_ind, col_ind, max(12, len(column_title) + 2))

    for row_ind, row in enumerate(report.rows, start=1):
        for col_ind, (column, value) in enumerate(zip(report.columns, row, strict=True)):
            if value is None or value == "":
                continue

            match column.type:
                case TypeOfColumn.INT | TypeOfColumn.CURRENCY | TypeOfColumn.PERCENTAGE:
                    if (number := parse_decimal(value)) is not None:
                        worksheet.write_number(row_ind, col_ind, float(number), formats.get(column.type))
                        continue
                case TypeOfColumn.DATETIME:
                    if dt := parse_datetime(value):
                        local_dt = dt.astimezone(tz).replace(tzinfo=None) if dt.tzinfo else dt
                        worksheet.write_datetime(row_ind, col_ind, local_dt, formats[TypeOfColumn.DATETIME])
                        continue

            # write_string never treats the value as a formula or URL
            worksheet.write_string(row_ind, col_ind, str(value))

    workbook.close()
    output_stream.write(buf.getvalue())
