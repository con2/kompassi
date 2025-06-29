from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pydantic
from django.conf import settings
from django.core.mail import send_mass_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.translation import get_language

from access.cbac import is_graphql_allowed_for_model
from dimensions.utils.dimension_cache import DimensionCache
from graphql_api.utils import get_message_in_language

from ..utils.lift_dimension_values import lift_dimension_values
from .enums import SurveyPurpose
from .response import Response
from .survey import Survey, SurveyApp

if TYPE_CHECKING:
    from involvement.models.involvement import Involvement


logger = logging.getLogger("kompassi")


class Workflow(pydantic.BaseModel, arbitrary_types_allowed=True):
    """
    The workflow defines automated actions that are triggered by events in the survey lifecycle.
    """

    survey: Survey

    @property
    def app(self) -> SurveyApp:
        return SurveyApp(self.survey.app_name)

    @classmethod
    def get_workflow(cls, survey: Survey):
        from program_v2.workflows.program_host_invitation import ProgramHostInvitationWorkflow
        from program_v2.workflows.program_offer import ProgramOfferWorkflow

        match SurveyApp(survey.app_name), survey.purpose:
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

    def handle_new_response_phase1(
        self,
        response: Response,
        old_version: Response | None = None,
    ):
        """
        Called when a new response is created for a survey using this workflow.
        Called during the transaction that creates the response.
        Do not call external services or perform any actions that require the transaction to be committed.
        """
        cache = self.survey.universe.preload_dimensions()

        if old_version:
            response.set_dimension_values(
                old_version.cached_dimensions,
                cache=cache,
            )
        else:
            response.set_dimension_values(self.survey.cached_default_dimensions, cache=cache)

        lift_dimension_values(response, cache=cache)
        response.refresh_cached_fields()

        # Old versions need not be findable through dimensions.
        if old_version:
            old_version.dimensions.all().delete()
            # triggers refresh_cached_dimensions for old_version, clearing cached_dimensions

        self.ensure_involvement(
            response,
            old_version=old_version,
            cache=response.event.involvement_universe.preload_dimensions(),
        )

        return cache

    def handle_new_response_phase2(
        self,
        response: Response,
        old_version: Response | None = None,
    ):
        """
        Called when a new response is created for a survey using this workflow.
        Called after the transaction that creates the response is committed.
        This is the place to call external services or perform any actions that require the transaction to be committed.
        """
        self.notify_subscribers(response, old_version=old_version)
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

    def ensure_involvement(
        self,
        response: Response,
        *,
        old_version: Response | None = None,
        cache: DimensionCache,
    ) -> Involvement | None:
        """
        If the response ought to result in Involvement, create it.
        """
        from involvement.models.involvement import Involvement

        if not response.survey.registry:
            return None

        return Involvement.from_survey_response(
            response=response,
            old_version=old_version,
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

        user = response.original_created_by
        if not user or not user.person:  # type: ignore
            return None, False

        return Badge.ensure(response.survey.event, user.person)  # type: ignore

    def notify_subscribers(
        self,
        response: Response,
        old_version: Response | None = None,
    ):
        from ..tasks import response_notify_subscribers

        response_notify_subscribers.delay(response.id, old_version.id if old_version else None)  # type: ignore

    def _notify_subscribers(
        self,
        response: Response,
        old_version: Response | None,
    ):
        # TODO recipient language instead of session language
        language = get_language()

        if (survey := response.survey) is None:
            raise TypeError("Cannot notify subscribers for a response that is not related to a survey")

        if (form := survey.get_form(language)) is None:
            raise TypeError("No form found in survey (this shouldn't happen)")

        if old_version:
            body_template_name = get_message_in_language(response.edited_response_message_templates, language)
            subject_template = get_message_in_language(response.edited_response_subject_templates, language)
        else:
            body_template_name = get_message_in_language(response.new_response_message_templates, language)
            subject_template = get_message_in_language(response.new_response_subject_templates, language)

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
                app=survey.app_name,
                operation="query",
                field="responses",
            )
        ]

        if not mailbag:
            return

        send_mass_mail(mailbag)  # type: ignore

    def response_can_be_edited_by(self, response: Response, request: HttpRequest) -> bool:
        """
        Check if the response can be edited by the user.
        This is a common method that checks both owner and admin editability.
        """
        return self.response_can_be_edited_by_owner(response, request) or self.response_can_be_edited_by_admin(
            response, request
        )

    def response_can_be_edited_by_owner(self, response: Response, request: HttpRequest) -> bool:
        """
        Common criteria for editability of a response shared by all workflows.
        """
        log_context: dict[str, str | dict[str, list[str]]] = dict(
            scope=response.survey.scope.slug,
            survey=response.survey.slug,
            response=response.id,
            created_by=response.revision_created_by.username if response.revision_created_by else None,
            logged_in_user=request.user.username if request.user.is_authenticated else None,  # type: ignore
        )

        if not request.user.is_authenticated:
            logger.info("Response not editable by owner (not logged in): %s", log_context)
            return False

        if not response.revision_created_by:
            logger.info("Response not editable by owner (revision_created_by unset): %s", log_context)
            return False

        if response.revision_created_by != request.user:
            logger.info("Response not editable by owner (not created by user): %s", log_context)
            return False

        if response.superseded_by is not None:
            logger.info("Response not editable by owner (not current version): %s", log_context)
            return False

        if not response.survey.responses_editable_until:
            logger.info("Response not editable by owner (responses_editable_until unset): %s", log_context)
            return False

        if now() >= self.survey.responses_editable_until:
            log_context["responses_editable_until"] = self.survey.responses_editable_until.isoformat()
            logger.info("Response not editable by owner (responses_editable_until passed): %s", log_context)
            return False

        locking_dimension_values = response.dimensions.filter(value__is_subject_locked=True)
        if locking_dimension_values.exists():
            locking_dimensions: dict[str, list[str]] = {}
            log_context["locking_dimensions"] = locking_dimensions
            for rdv in locking_dimension_values:
                locking_dimensions.setdefault(rdv.value.dimension.slug, []).append(rdv.value.slug)

            logger.info("Response not editable by owner (subject locked dimensions): %s", log_context)
            return False

        logger.info("Response editable by owner: %s", log_context)
        return True

    def response_can_be_edited_by_admin(
        self,
        response: Response,
        request: HttpRequest,
    ) -> bool:
        return response.superseded_by is None and is_graphql_allowed_for_model(
            request.user,
            instance=response.survey,
            app=response.survey.app_name,
            operation="update",
            field="responses",
        )

    # TODO(#714) Reconcile with Survey.can_responses_be_deleted_by
    def response_can_be_deleted_by(
        self,
        response: Response,
        request: HttpRequest,
    ) -> bool:
        return (
            not response.survey.protect_responses
            and response.is_current_version
            and is_graphql_allowed_for_model(
                request.user,
                instance=response.survey,
                app=response.survey.app_name,
                operation="delete",
                field="responses",
            )
        )

    def response_can_be_accepted_by(
        self,
        response: Response,
        request: HttpRequest,
    ) -> bool:
        """
        The default workflow does not have the notion of accepting a response.
        """
        return False

    def response_can_be_cancelled_by(
        self,
        response: Response,
        request: HttpRequest,
    ) -> bool:
        """
        The default workflow does not have the notion of cancelling a response.
        """
        return False
