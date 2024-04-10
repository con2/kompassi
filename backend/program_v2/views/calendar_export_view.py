from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from core.models.event import Event
from forms.utils.process_form_data import FALSY_VALUES
from graphql_api.language import DEFAULT_LANGUAGE

from ..calendar_export import export_program_response
from ..models.program import Program


# TODO add test for this view
def calendar_export_view(request: HttpRequest, event_slug: str):
    event = get_object_or_404(Event, slug=event_slug)
    filters: dict[str, list[str]] = {k: [str(v) for v in vs] for k, vs in request.GET.lists()}
    language = filters.pop("language", [DEFAULT_LANGUAGE])[0]
    programs = Program.objects.filter(event=event)

    # filter programs by slug (may be ?slug=a&slug=b or ?slug=a,b,c)
    slugs = [slug for slugs in filters.pop("slug", []) for slug in slugs.split(",")]
    if slugs:
        programs = programs.filter(slug__in=slugs)

    # filter programs by favorited status
    favorited = filters.pop("favorited", [])
    if any(v.lower() not in FALSY_VALUES for v in favorited):
        if request.user.is_authenticated:
            programs = programs.filter(favorited_by=request.user)
        else:
            programs = programs.none()

    # filter programs by dimensions
    # TODO encapsulate this logic in a helper function
    for dimension_slug, value_slugs in filters.items():
        value_slugs = [slug for slugs in value_slugs for slug in slugs.split(",")]
        programs = programs.filter(
            dimensions__dimension__slug=dimension_slug,
            dimensions__value__slug__in=value_slugs,
        )

    return export_program_response(programs, language=language)


def single_program_calendar_export_view(request: HttpRequest, event_slug: str, program_slug: str):
    program = get_object_or_404(Program, event__slug=event_slug, slug=program_slug)
    return export_program_response([program], language=request.GET.get("language", DEFAULT_LANGUAGE))
