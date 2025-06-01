from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from access.cbac import graphql_check_instance
from core.models import Event
from dimensions.filters import DimensionFilters
from event_log_v2.utils.emit import emit

from ..excel_export import write_responses_as_excel
from ..models.survey import Survey


def forms_survey_excel_export_view(
    request: HttpRequest,
    event_slug: str | None,
    survey_slug: str,
):
    timestamp = now().strftime("%Y%m%d%H%M%S")
    # TODO survey.scope instead of survey.event
    event = get_object_or_404(Event, slug=event_slug)
    survey = get_object_or_404(Survey, event=event, slug=survey_slug)
    filename = f"{event.slug}_{survey.slug}_responses_{timestamp}.xlsx"

    # TODO(#324): Failed check causes 500 now, turn it to 403 (middleware?)
    graphql_check_instance(
        survey,
        request,
        app=survey.app,
        field="responses",
        operation="query",
    )

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    responses = DimensionFilters.from_query_dict(request.GET).filter(survey.current_responses.all())

    if survey.profile_field_selector:
        emit("core.person.exported", request=request)

    write_responses_as_excel(
        survey,
        survey.dimensions.order_by("order"),
        survey.combined_fields,
        responses.only("form_data").order_by("revision_created_at"),
        response,
    )

    return response
