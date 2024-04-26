from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from access.cbac import graphql_check_instance
from core.models import Event

from ..excel_export import write_responses_as_excel
from ..models.survey import Survey


def forms_survey_excel_export_view(
    request: HttpRequest,
    event_slug: str | None,
    survey_slug: str,
):
    timestamp = now().strftime("%Y%m%d%H%M%S")

    if event_slug:
        event = get_object_or_404(Event, slug=event_slug)
        survey = get_object_or_404(Survey, event=event, slug=survey_slug)
        filename = f"{event.slug}_{survey.slug}_responses_{timestamp}.xlsx"
    else:
        survey = get_object_or_404(Survey, event__isnull=True, slug=survey_slug)
        filename = f"{survey.slug}_responses_{timestamp}.xlsx"

    # TODO(#324): Failed check causes 500 now, turn it to 403 (middleware?)
    graphql_check_instance(survey, request, "responses", "query")

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    write_responses_as_excel(
        survey.dimensions.order_by("order"),
        survey.combined_fields,
        survey.responses.order_by("created_at").only("form_data"),
        response,
    )

    return response
