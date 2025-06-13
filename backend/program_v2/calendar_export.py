from collections.abc import Iterable
from typing import TextIO

from django.http import HttpResponse
from ics import Calendar
from ics import Event as CalendarEvent

from core.utils.locale_utils import get_message_in_language
from graphql_api.language import DEFAULT_LANGUAGE

from .models.program import Program


def export_programs(
    programs: Iterable[Program],
    output_stream: TextIO | HttpResponse,
    language=DEFAULT_LANGUAGE,
):
    calendar = Calendar()
    for program in programs:
        for schedule_item in program.schedule_items.all():
            event = CalendarEvent()
            event.name = schedule_item.title
            event.begin = schedule_item.start_time
            event.end = schedule_item.cached_end_time
            event.description = program.description.replace("\r", "")
            event.location = get_message_in_language(schedule_item.cached_location, language)
            calendar.events.add(event)

    output_stream.writelines(calendar.serialize_iter())


def export_program_response(
    programs: Iterable[Program],
    language=DEFAULT_LANGUAGE,
):
    response = HttpResponse(content_type="text/calendar")
    response["Content-Disposition"] = "attachment; filename=program.ics"
    export_programs(programs, response, language=language)
    return response
