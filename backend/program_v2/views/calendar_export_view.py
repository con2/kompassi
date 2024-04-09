from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from core.models.event import Event
from graphql_api.language import DEFAULT_LANGUAGE

from ..calendar_export import export_program_response
from ..models.program import Program


def calendar_export_view(request: HttpRequest, event_slug: str):
    event = get_object_or_404(Event, slug=event_slug)
    language = request.GET.get("language") or DEFAULT_LANGUAGE
    programs = Program.objects.filter(event=event)
    return export_program_response(programs, language=language)
