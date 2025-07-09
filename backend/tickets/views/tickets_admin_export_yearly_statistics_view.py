import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

from django.db import connection
from django.http import HttpResponse

from core.models.event import Event
from core.utils.pkg_resources_compat import resource_string

from ..helpers import tickets_admin_required

STATISTICS_QUERY = resource_string(__name__, "queries/event_statistics.sql").decode("utf-8")


@dataclass
class QueryRow:
    event_id: int
    sales_date: date
    days_to_event: int
    total_tickets_sold: int
    total_amount_cents: int


@dataclass
class ResultRowEvent:
    sales_date: date
    total_tickets_sold: int
    total_amount_cents: int
    cumulative_tickets_sold: int
    cumulative_amount_cents: int


@tickets_admin_required
def tickets_admin_export_yearly_statistics_view(request, vars, event: Event):
    events = [
        event
        for event in event.organization.events.filter(
            start_time__isnull=False,
            ticketseventmeta__isnull=False,
        ).order_by("start_time")
        if event.tickets_event_meta.is_user_admin(request.user)
    ]
    event_ids = [event.id for event in events]

    response = HttpResponse()
    response["Content-Type"] = "text/csv"
    response["Content-Disposition"] = 'attachment; filename="sales-statistics.csv"'

    # event id -> days to event -> cumulative tickets (or euros)
    rows_by_event_by_days: defaultdict[int, dict[int, QueryRow]] = defaultdict(dict)

    cursor = connection.cursor()
    cursor.execute(STATISTICS_QUERY, [event_ids])
    for row in cursor.fetchall():
        row = QueryRow(*row)
        rows_by_event_by_days[row.event_id][row.days_to_event] = row

    # pivot from long to wide format
    # days to event -> event_id -> (date, number_of_tickets, number_of_euros) per event
    result: defaultdict[int, list[ResultRowEvent]] = defaultdict(list)

    # negative is before event, zero is first day of event
    start_days = min(min(rows_by_days.keys()) for rows_by_days in rows_by_event_by_days.values())
    end_days = max(max(rows_by_days.keys()) for rows_by_days in rows_by_event_by_days.values())

    for compare_event in events:
        cumulative_tickets = 0
        cumulative_amount = 0

        for days_to_event in range(start_days, end_days + 1):
            row = rows_by_event_by_days[compare_event.id].get(days_to_event)

            if compare_event.start_time is None:
                raise AssertionError("This will not happen (filtered in query) but Pyrekt doesn't know that")

            sales_date = row.sales_date if row else compare_event.start_time.date() + timedelta(days=days_to_event)
            cumulative_tickets += row.total_tickets_sold if row else 0
            cumulative_amount += row.total_amount_cents if row else 0

            result[days_to_event].append(
                ResultRowEvent(
                    sales_date=sales_date,
                    total_tickets_sold=row.total_tickets_sold if row else 0,
                    total_amount_cents=row.total_amount_cents if row else 0,
                    cumulative_tickets_sold=cumulative_tickets,
                    cumulative_amount_cents=cumulative_amount,
                )
            )

    csv_writer = csv.writer(response)

    header_row = ["Days to event"]
    for compare_event in events:
        header_row.extend(
            [
                f"Date ({compare_event.name})",
                f"Daily tickets ({compare_event.name})",
                f"Daily euros ({compare_event.name})",
                f"Cumulative tickets ({compare_event.name})",
                f"Cumulative euros ({compare_event.name})",
            ]
        )
    csv_writer.writerow(header_row)

    today = datetime.now().date()
    for days_to_event in range(start_days, end_days + 1):
        event_rows = result[days_to_event]
        result_row: list[Any] = [days_to_event]

        for event_row in event_rows:
            if event_row.sales_date <= today:
                result_row.extend(
                    [
                        event_row.sales_date,
                        event_row.total_tickets_sold,
                        event_row.total_amount_cents / 100,
                        event_row.cumulative_tickets_sold,
                        event_row.cumulative_amount_cents / 100,
                    ]
                )
            else:
                # no useful info in future dates, so omit the data
                result_row.extend([event_row.sales_date, "", "", "", ""])

        csv_writer.writerow(result_row)

    return response
