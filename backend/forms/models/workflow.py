from __future__ import annotations

import logging

import pydantic
from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.utils.translation import get_language

from access.cbac import is_graphql_allowed_for_model
from dimensions.utils.dimension_cache import DimensionCache
from graphql_api.utils import get_message_in_language

from ..utils.lift_dimension_values import lift_dimension_values
from .enums import SurveyPurpose
from .response import Response
from .survey import Survey, SurveyApp

logger = logging.getLogger("kompassi")


class Workflow(pydantic.BaseModel, arbitrary_types_allowed=True):
    """
    The workflow defines automated actions that are triggered by events in the survey lifecycle.
    """

    survey: Survey

    @property
    def app(self) -> SurveyApp:
        return SurveyApp(self.survey.app)

    @classmethod
    def get_workflow(cls, survey: Survey):
        from program_v2.workflows.program_host_invitation import ProgramHostInvitationWorkflow
        from program_v2.workflows.program_offer import ProgramOfferWorkflow

        match SurveyApp(survey.app), survey.purpose:
            case SurveyApp.PROGRAM_V2, SurveyPurpose.DEFAULT:
                return ProgramOfferWorkflow(survey=survey)
            case SurveyApp.PROGRAM_V2, SurveyPurpose.INVITE:
                return ProgramHostInvitationWorkflow(survey=survey)
            case _:
                return cls(survey=survey)

    def is_response_active(self, response: Response) -> bool:
        # The basic survey workflow does not have a concept of active/inactive responses.
        return True

    def handle_new_survey(self):
        """
        Called when a new form is created for a survey using this workflow.
        """
        pass

    def handle_form_update(self):
        """
        Called when a form of a survey using this workflow is created, deleted or updated.
        Not called for form field updates.
        """
        pass

    def handle_new_response_phase1(self, response: Response):
        """
        Called when a new response is created for a survey using this workflow.
        Called during the transaction that creates the response.
        Do not call external services or perform any actions that require the transaction to be committed.
        """
        cache = self.survey.universe.preload_dimensions()
        response.set_dimension_values(self.survey.cached_default_dimensions, cache=cache)
        lift_dimension_values(response, cache=cache)
        response.refresh_cached_fields()

        self.ensure_involvement(
            response,
            cache=response.event.involvement_universe.preload_dimensions(),
        )

        return cache

    def handle_new_response_phase2(self, response: Response):
        """
        Called when a new response is created for a survey using this workflow.
        Called after the transaction that creates the response is committed.
        This is the place to call external services or perform any actions that require the transaction to be committed.
        """
        self.notify_subscribers(response)
        self.ensure_survey_to_badge(response)

    def handle_response_dimension_update(self, response: Response):
        """
        Called when dimension values of a response are updated.
        Called after the transaction that updates the response dimensions is committed.
        Not called for newly created responses.
        """
        self.ensure_involvement(
            response,
            cache=response.event.involvement_universe.preload_dimensions(),
        )
        self.ensure_survey_to_badge(response)

    def ensure_involvement(self, response: Response, cache: DimensionCache):
        """
        If the response ought to result in Involvement, create it.
        """
        from involvement.models.involvement import Involvement

        if not response.survey.registry:
            return

        Involvement.from_survey_response(
            response=response,
            cache=cache,
        )

    def ensure_survey_to_badge(self, response: Response):
        """
        Invoke Survey to Badge (STB) for new responses.
        See https://outline.con2.fi/doc/survey-to-badge-stb-mxK1UW6hAn

        TODO Deprecate in favor of Involvement
        """
        from badges.models.badge import Badge
        from badges.models.survey_to_badge import SurveyToBadgeMapping

        if not SurveyToBadgeMapping.objects.filter(survey=response.survey).exists():
            return None, False

        user = response.created_by
        if not user or not user.person:
            return None, False

        return Badge.ensure(response.survey.event, user.person)

    def notify_subscribers(self, response: Response):
        from ..tasks import response_notify_subscribers

        response_notify_subscribers.delay(response.id)  # type: ignore

    def _notify_subscribers(self, response: Response):
        # TODO recipient language instead of session language
        language = get_language()

        if (survey := response.survey) is None:
            raise TypeError("Cannot notify subscribers for a response that is not related to a survey")

        if (form := survey.get_form(language)) is None:
            raise TypeError("No form found in survey (this shouldn't happen)")

        body_template_name = get_message_in_language(response.notification_templates, language)
        subject_template = get_message_in_language(response.subject_templates, language)

        if not body_template_name or not subject_template:
            raise ValueError("Missing body or subject template for supported language", language)

        vars = dict(
            survey_title=form.title,
            event_name=survey.event.name,
            response_url=response.admin_url,
            sender_email=settings.DEFAULT_FROM_EMAIL,
        )

        subject = subject_template.format(**vars)
        body = render_to_string(body_template_name, vars)
        mailbag = []

        if settings.DEBUG:
            logger.debug(subject)
            logger.debug(body)

        mailbag = [
            (subject, body, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
            for subscriber in survey.subscribers.all()
            if is_graphql_allowed_for_model(
                subscriber,
                instance=survey,
                operation="query",
                field="responses",
            )
        ]

        send_mass_mail(mailbag)  # type: ignore
