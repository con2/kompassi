from typing import Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from access.cbac import default_cbac_required
from core.models import Event

from ..models.survey import EventSurvey, GlobalSurvey
from ..models.form_response import EventFormResponse, GlobalFormResponse
from ..excel_export import write_responses_as_excel
from ..utils.merge_form_fields import merge_fields


@default_cbac_required
def forms_survey_excel_export_view(request: HttpRequest, event_slug: Optional[str], survey_slug: str):
    timestamp = now().strftime("%Y%m%d%H%M%S")

    if event_slug:
        event = get_object_or_404(Event, slug=event_slug)
        survey = get_object_or_404(EventSurvey, event=event, slug=survey_slug)
        languages = survey.languages.all()
        responses = EventFormResponse.objects.filter(form__in=languages)
        filename = f"{event.slug}_{survey.slug}_responses_{timestamp}.xlsx"
    else:
        survey = get_object_or_404(GlobalSurvey, slug=survey_slug)
        languages = survey.languages.all()
        responses = GlobalFormResponse.objects.filter(form__in=languages)
        filename = f"{survey.slug}_responses_{timestamp}.xlsx"

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    fields = merge_fields(survey.languages.all())

    write_responses_as_excel(fields, responses.order_by("created_at").only("form_data"), response)

    return response
