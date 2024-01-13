from django.utils.translation import gettext_lazy as _

from event_log import registry

registry.register(
    name="surveys.globalsurveyresult.created",
    message=_("New survey answer: {entry.global_survey_result.survey.title}"),
    email_body_template="survey_result_created.eml",
)

registry.register(
    name="surveys.eventsurveyresult.created",
    message=_("New survey answer: {entry.event_survey_result.survey.title}"),
    email_body_template="survey_result_created.eml",
)
