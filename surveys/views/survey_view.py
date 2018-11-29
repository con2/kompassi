import json

from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from csp.decorators import csp_update
from ipware.ip import get_ip

from core.models import Event

from ..models import EventSurvey, EventSurveyResult, GlobalSurvey, GlobalSurveyResult


@require_http_methods(['GET', 'HEAD', 'POST'])
@csp_update(SCRIPT_SRC=['cdnjs.cloudflare.com'])
def survey_view(request, event_slug='', survey_slug=''):
    if event_slug:
        event = get_object_or_404(Event, slug=event_slug)
        survey = get_object_or_404(EventSurvey, event=event, slug=survey_slug, is_active=True)
        SurveyResult = EventSurveyResult
    else:
        event = None
        survey = get_object_or_404(GlobalSurvey, slug=survey_slug, is_active=True)
        SurveyResult = GlobalSurveyResult

    if request.method == 'POST':
        try:
            result_model = json.loads(request.body)
        except (TypeError, ValueError):
            return HttpResponse(status=400)

        result = SurveyResult(
            survey=survey,
            author=request.user if request.user.is_authenticated else None,
            author_ip_address=get_ip(request) or '',
            model=result_model,
        )

        result.save()

    vars = dict(
        event=event,
        model_json=json.dumps(survey.model),
        survey=survey,
    )

    return render(request, 'survey_view.pug', vars)
