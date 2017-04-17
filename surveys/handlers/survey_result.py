from event_log.utils import log_creations, INSTANCE

from ..models import GlobalSurveyResult, EventSurveyResult


log_creations(
    GlobalSurveyResult,
    global_survey_result=INSTANCE,
)


log_creations(
    EventSurveyResult,
    event_survey_result=INSTANCE,
    event=lambda instance: instance.survey.event,
)
