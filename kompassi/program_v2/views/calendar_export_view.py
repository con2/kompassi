from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE

from ..calendar_export import export_program_response
from ..filters import ProgramFilters
from ..models.program import Program


# TODO add test for this view
def calendar_export_view(request: HttpRequest, event_slug: str):
    event = get_object_or_404(Event, slug=event_slug)
    meta = event.program_v2_event_meta
    if meta is None or not meta.is_schedule_public:
        return HttpResponseNotFound()
    filters: dict[str, list[str]] = {k: [str(v) for v in vs] for k, vs in request.GET.lists()}
    language = filters.pop("language", [DEFAULT_LANGUAGE])[0]
    programs = Program.objects.filter(event=event)
    programs = ProgramFilters.from_query_dict(filters).filter_program(programs, user=request.user)
    return export_program_response(programs, language=language)


def single_program_calendar_export_view(request: HttpRequest, event_slug: str, program_slug: str):
    event = get_object_or_404(Event, slug=event_slug)
    meta = event.program_v2_event_meta
    if meta is None or not meta.is_schedule_public:
        return HttpResponseNotFound()
    program = get_object_or_404(Program, event=event, slug=program_slug)
    return export_program_response([program], language=request.GET.get("language", DEFAULT_LANGUAGE))
