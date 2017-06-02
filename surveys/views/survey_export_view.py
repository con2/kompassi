from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.decorators.http import require_safe

from core.csv_export import CSV_EXPORT_FORMATS, csv_response
from core.models import Event

from ..models import EventSurvey, EventSurveyResult, GlobalSurvey, GlobalSurveyResult


# TODO: more finer grained access control
@user_passes_test(lambda u: u.is_superuser)
@require_safe
def survey_export_view(request, event_slug='', survey_slug='', format='xlsx'):
    if event_slug:
        event = get_object_or_404(Event, slug=event_slug)
        survey = get_object_or_404(EventSurvey, event=event, slug=survey_slug, is_active=True)
        SurveyResult = EventSurveyResult
        slug = f'{event.slug}-{survey.slug}'
    else:
        event = None
        survey = get_object_or_404(GlobalSurvey, slug=survey_slug, is_active=True)
        SurveyResult = GlobalSurveyResult
        slug = survey.slug

    results = SurveyResult.objects.filter(survey=survey).order_by('created_at')
    timestamp = now().strftime('%Y%m%d%H%M%S')

    filename = f'{slug}-results-{timestamp}.{format}'

    return csv_response(
        event,
        SurveyResult,
        results,
        filename=filename,
        dialect=CSV_EXPORT_FORMATS[format],
        m2m_mode='comma_separated'
    )
