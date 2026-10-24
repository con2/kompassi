from __future__ import annotations

from collections.abc import Callable
from datetime import tzinfo
from zoneinfo import ZoneInfo

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from kompassi.access.cbac import graphql_check_instance, graphql_check_model
from kompassi.core.models.event import Event
from kompassi.core.reports.kompassi_stats import kompassi_stats_reports
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.involvement.emperkelators.base import BaseEmperkelator
from kompassi.involvement.models.involvement import Involvement
from kompassi.program_v2.models import ScheduleItem
from kompassi.program_v2.reports import get_reports as get_program_reports
from kompassi.tickets_v2.reports import get_reports as get_tickets_reports

from .export import CONTENT_TYPES, ExportFormat, get_filename, write_csv, write_xlsx
from .models.report import Report


def _tickets_reports(request: HttpRequest, event: Event, lang: str) -> list[Report]:
    if not (meta := event.tickets_v2_event_meta):
        raise Http404("Event does not use Tickets V2")
    # same check as TicketsV2EventMetaType.resolve_reports
    graphql_check_instance(meta, request, field="reports")
    return get_tickets_reports(event, lang)


def _program_reports(request: HttpRequest, event: Event, lang: str) -> list[Report]:
    if not (meta := event.program_v2_event_meta):
        raise Http404("Event does not use Program V2")
    # same check as ProgramV2EventMetaType.resolve_reports
    graphql_check_model(ScheduleItem, event.scope, request)
    return get_program_reports(meta, lang)


def _involvement_reports(request: HttpRequest, event: Event, lang: str) -> list[Report]:
    if not (meta := event.involvement_event_meta):
        raise Http404("Event does not use Involvement")
    # same check as InvolvementEventMetaType.resolve_reports
    graphql_check_model(Involvement, event.scope, request)
    Emperkelator = meta.emperkelator_class or BaseEmperkelator
    return Emperkelator.get_reports(event, lang)


REPORT_SOURCES: dict[str, Callable[[HttpRequest, Event, str], list[Report]]] = dict(
    tickets=_tickets_reports,
    program=_program_reports,
    involvement=_involvement_reports,
)


def _export_response(
    reports: list[Report],
    report_slug: str,
    filename_prefix: str,
    tz: tzinfo,
    format: ExportFormat,
    lang: str,
) -> HttpResponse:
    report = next((report for report in reports if report.slug == report_slug), None)
    if report is None:
        raise Http404("No such report")

    filename = get_filename(report, filename_prefix, tz, format)
    response = HttpResponse(content_type=CONTENT_TYPES[format])
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    match format:
        case "csv":
            write_csv(report, lang, response)
        case "xlsx":
            write_xlsx(report, lang, tz, response)

    return response


@require_safe
def event_report_export_view(
    request: HttpRequest,
    event_slug: str,
    source: str,
    report_slug: str,
    format: ExportFormat,
):
    event = get_object_or_404(Event, slug=event_slug)
    lang = request.GET.get("lang") or DEFAULT_LANGUAGE
    reports = REPORT_SOURCES[source](request, event, lang)
    return _export_response(reports, report_slug, event.slug, event.timezone, format, lang)


@require_safe
def stats_report_export_view(
    request: HttpRequest,
    report_slug: str,
    format: ExportFormat,
):
    """
    The site-wide statistics at /stats are public, as is the GraphQL field behind them.
    """
    lang = request.GET.get("lang") or DEFAULT_LANGUAGE
    reports = kompassi_stats_reports(lang)
    return _export_response(reports, report_slug, "kompassi", ZoneInfo(settings.TIME_ZONE), format, lang)
