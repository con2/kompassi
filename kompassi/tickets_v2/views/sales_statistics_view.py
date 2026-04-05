import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from kompassi.access.cbac import is_graphql_allowed
from kompassi.core.models.event import Event

SQL_DIR = Path(__file__).parent / "sql"
STATISTICS_QUERY = (SQL_DIR / "event_statistics.sql").read_text()


@dataclass
class QueryRow:
    event_id: int
    order_date: date
    days_to_event: int
    total_tickets_sold: int
    total_amount: Decimal


@dataclass
class ResultRowEvent:
    sales_date: date
    total_tickets_sold: int
    total_amount: Decimal
    cumulative_tickets_sold: int
    cumulative_amount: Decimal


def _is_tickets_admin(user, event: Event) -> bool:
    return is_graphql_allowed(
        user,
        scope=event.scope,
        operation="query",
        app="tickets_v2",
        model="Order",
        field="self",
    )


@login_required
def sales_statistics_view(request: HttpRequest, event_slug: str) -> HttpResponse:
    event = get_object_or_404(Event, slug=event_slug)

    if not _is_tickets_admin(request.user, event):
        return HttpResponse("Permission denied", status=403)

    events = [
        e
        for e in Event.objects.filter(
            organization=event.organization,
            start_time__isnull=False,
            ticketsv2eventmeta__isnull=False,
        ).order_by("start_time")
        if _is_tickets_admin(request.user, e)
    ]
    event_ids = [e.id for e in events]

    rows_by_event_by_days: defaultdict[int, dict[int, QueryRow]] = defaultdict(dict)

    with connection.cursor() as cursor:
        cursor.execute(STATISTICS_QUERY, [event_ids])
        for row in cursor.fetchall():
            query_row = QueryRow(*row)
            rows_by_event_by_days[query_row.event_id][query_row.days_to_event] = query_row

    # Only include events that have at least one paid order
    events_with_data = [e for e in events if rows_by_event_by_days[e.id]]
    if not events_with_data:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="sales-statistics.csv"'
        return response

    start_days = min(min(rows.keys()) for rows in rows_by_event_by_days.values() if rows)
    end_days = max(max(rows.keys()) for rows in rows_by_event_by_days.values() if rows)

    # pivot from long to wide format
    # days_to_event -> list of ResultRowEvent, one per event
    result: defaultdict[int, list[ResultRowEvent]] = defaultdict(list)

    for compare_event in events:
        cumulative_tickets = 0
        cumulative_amount = Decimal(0)

        for days_to_event in range(start_days, end_days + 1):
            row = rows_by_event_by_days[compare_event.id].get(days_to_event)

            if compare_event.start_time is None:
                raise AssertionError("This will not happen (filtered in query) but type checker doesn't know that")

            sales_date = row.order_date if row else compare_event.start_time.date() + timedelta(days=days_to_event)
            cumulative_tickets += row.total_tickets_sold if row else 0
            cumulative_amount += row.total_amount if row else Decimal(0)

            result[days_to_event].append(
                ResultRowEvent(
                    sales_date=sales_date,
                    total_tickets_sold=row.total_tickets_sold if row else 0,
                    total_amount=row.total_amount if row else Decimal(0),
                    cumulative_tickets_sold=cumulative_tickets,
                    cumulative_amount=cumulative_amount,
                )
            )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="sales-statistics.csv"'
    csv_writer = csv.writer(response)

    header_row: list[Any] = ["Days to event"]
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

    today = date.today()
    for days_to_event in range(start_days, end_days + 1):
        event_rows = result[days_to_event]
        result_row: list[Any] = [days_to_event]

        for event_row in event_rows:
            if event_row.sales_date <= today:
                result_row.extend(
                    [
                        event_row.sales_date,
                        event_row.total_tickets_sold,
                        event_row.total_amount,
                        event_row.cumulative_tickets_sold,
                        event_row.cumulative_amount,
                    ]
                )
            else:
                result_row.extend([event_row.sales_date, "", "", "", ""])

        csv_writer.writerow(result_row)

    return response
