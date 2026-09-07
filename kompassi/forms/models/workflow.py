from __future__ import annotations

import logging
from datetime import timedelta
from functools import cached_property
from typing import TYPE_CHECKING

import pydantic
from django.conf import settings
from django.core.mail import send_mass_mail
from django.db.models import Q, QuerySet
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.translation import get_language
from graphene import ResolveInfo

from kompassi.access.cbac import Operation, make_graphql_claims, raise_cbac_permission_denied
from kompassi.access.constants import CBAC_VALID_AFTER_EVENT_DAYS
from kompassi.access.models.cbac_entry import CBACEntry, Claims
from kompassi.core.utils import log_get_or_create
from kompassi.dimensions.utils.dimension_cache import DimensionCache
from kompassi.event_log_v2.utils.emit import emit
from kompassi.graphql_api.utils import get_message_in_language
from kompassi.involvement.filters import InvolvementFilters

from ..utils.lift_dimension_values import lift_dimension_values
from .enums import CanResponsesBeDeleted, SurveyPurpose
from .response import Response
from .survey import DimensionApp, Survey

if TYPE_CHECKING:
    from kompassi.core.models.person import Person
    from kompassi.involvement.models.involvement import Involvement


logger = logging.getLogger(__name__)


class Workflow(pydantic.BaseModel, arbitrary_types_allowed=True):
    """
    The workflow defines automated actions that are triggered by events in the survey lifecycle.
    """

    survey: Survey

    @property
    def app(self) -> DimensionApp:
        return self.survey.app

    @property
    def protect_responses(self) -> bool:
        """
        Whether responses to this survey are currently protected from deletion.
        Overridden by workflows whose app protects responses at a different
        granularity than per-survey (see eg. ProgramOfferWorkflow).
        """
        return self.survey.protect_responses

    @property
    def access_root_claims(self) -> Claims:
        """
        Claims that root access checks at this survey. Program workflows return {}
        because program forms are governed by event-wide program_v2 admin rights.
        """
        return {"survey": self.survey.slug}

    @property
    def can_access_be_granted(self) -> bool:
        return bool(self.access_root_claims)

    @cached_property
    def grant_claimses(self) -> list[Claims]:
        """
        Claims of the CBAC entries a per-survey grant consists of: one rooted at the survey,
        one rooted at its dimension universe. Empty if access cannot be granted per survey.
        Must stay in sync with Universe.access_root_claims.
        """
        if not self.can_access_be_granted:
            return []

        survey = self.survey
        organization = survey.scope.organization
        if organization is None:
            raise AssertionError(f"Survey {survey} has no organization")

        return [
            {
                "organization": organization.slug,
                "event": survey.event.slug,
                "app": survey.app.app_name,
                **self.access_root_claims,
            },
            {
                "organization": organization.slug,
                "event": survey.event.slug,
                "app": survey.universe.app.app_name,
                **survey.universe.access_root_claims,
            },
        ]

    def make_claims(self, *, operation: Operation, field: str = "self", instance=None) -> Claims:
        if instance is None:
            instance = self.survey

        extra: Claims = dict(self.access_root_claims)
        slug = getattr(instance, "slug", None)
        if slug is not None:
            extra.setdefault("slug", slug)

        return make_graphql_claims(
            scope=self.survey.scope,
            operation=operation,
            app=self.survey.app,
            model=instance.__class__.__name__,
            field=field,
            **extra,
        )

    def is_allowed_for_user(self, user, *, operation: Operation, field: str = "self", instance=None) -> bool:
        """
        Like is_allowed, but takes a user instead of a request. Used where there is no
        request at hand, eg. when checking subscribers for response notifications.
        """
        return CBACEntry.is_allowed(user, self.make_claims(operation=operation, field=field, instance=instance))

    def is_allowed(self, request: HttpRequest, *, operation: Operation, field: str = "self", instance=None) -> bool:
        claims = self.make_claims(operation=operation, field=field, instance=instance)

        cache = getattr(request, "kompassi_cache", None)
        if cache is not None:
            return cache.has_cbac_permission(claims)

        return CBACEntry.is_allowed(request.user, claims)

    def check_access(
        self,
        info_or_request: ResolveInfo | HttpRequest,
        *,
        operation: Operation,
        field: str = "self",
        instance=None,
    ) -> None:
        request: HttpRequest = info_or_request.context if isinstance(info_or_request, ResolveInfo) else info_or_request

        if not self.is_allowed(request, operation=operation, field=field, instance=instance):
            raise_cbac_permission_denied(request, self.make_claims(operation=operation, field=field, instance=instance))

    @property
    def access_grants(self) -> QuerySet[CBACEntry]:
        """
        Users who have been granted per-survey access to this survey, ie. the entries
        that grant_access creates rooted at the survey (not at its universe).
        """
        if not self.can_access_be_granted:
            return CBACEntry.objects.none()

        return (
            CBACEntry.objects.filter(
                claims=self.grant_claimses[0],
                valid_until__gte=now(),
                user__person__isnull=False,
            )
            .select_related("user__person")
            .order_by("user__person__surname", "user__person__first_name")
        )

    def grantable_people(self, search: str = "", limit: int = 20) -> QuerySet[Person]:
        """
        Persons who can be granted access to this survey: those with an active
        Involvement in the event who have a user account and do not already have access.
        """
        from kompassi.core.models.person import Person

        involvements = InvolvementFilters(search=search).filter(
            self.survey.event.involvement_universe.active_involvements
        )

        return (
            Person.objects.filter(id__in=involvements.values("person_id"), user__isnull=False)
            .exclude(user__in=self.access_grants.values("user_id"))
            .order_by("surname", "first_name")[:limit]
        )

    def grant_access(self, person: Person, request: HttpRequest) -> list[CBACEntry]:
        if not self.can_access_be_granted:
            raise ValueError("Access cannot be granted per survey for this workflow")

        if person.user is None:
            raise ValueError(f"{person} does not have a user account")

        event = self.survey.event
        if not event.involvement_universe.active_involvements.filter(person=person).exists():
            raise ValueError(f"{person} does not have an active involvement in {event}")

        if event.end_time is None:
            raise ValueError(f"{event} has no end time")

        valid_until = event.end_time + timedelta(days=CBAC_VALID_AFTER_EVENT_DAYS)
        if valid_until < now():
            raise ValueError(f"{event} ended too long ago to grant access")

        entries = []
        for claims in self.grant_claimses:
            entry = CBACEntry.objects.filter(user=person.user, claims=claims, valid_until__gte=now()).first()
            created = entry is None

            if created:
                entry = CBACEntry.objects.create(
                    user=person.user,
                    claims=claims,
                    valid_from=now(),
                    valid_until=valid_until,
                    created_by=request.user,
                )

            log_get_or_create(logger, entry, created)
            if created:
                emit("access.cbacentry.created", request=request, other_fields=entry.as_dict())

            entries.append(entry)

        return entries

    def revoke_access(self, person: Person, request: HttpRequest) -> int:
        if not self.can_access_be_granted or person.user is None:
            return 0

        query = Q()
        for claims in self.grant_claimses:
            query |= Q(claims=claims)

        entries = CBACEntry.objects.filter(query, user=person.user)

        count = 0
        for entry in entries:
            emit("access.cbacentry.deleted", request=request, other_fields=entry.as_dict())
            count += 1

        entries.delete()
        return count

    def revoke_all_access(self, request: HttpRequest | None) -> int:
        """
        Deletes every CBACEntry granted via grant_access for this survey, regardless of
        grantee. Call this when the survey itself is deleted: the survey's Universe is not
        deleted along with it (see Survey._get_universe), so a future survey created with
        the same slug would otherwise reuse the same Universe and inherit these grants.
        """
        if not self.can_access_be_granted:
            return 0

        query = Q()
        for claims in self.grant_claimses:
            query |= Q(claims=claims)

        entries = CBACEntry.objects.filter(query)

        count = 0
        for entry in entries:
            emit("access.cbacentry.deleted", request=request, other_fields=entry.as_dict())
            count += 1

        entries.delete()
        return count

    @classmethod
    def get_workflow(cls, survey: Survey):
        from kompassi.program_v2.workflows.program_host_invitation import ProgramHostInvitationWorkflow
        from kompassi.program_v2.workflows.program_offer import ProgramOfferWorkflow

        match survey.app, survey.purpose:
            case DimensionApp.PROGRAM, SurveyPurpose.DEFAULT:
                return ProgramOfferWorkflow(survey=survey)
            case DimensionApp.PROGRAM, SurveyPurpose.INVITE:
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

    def handle_form_update(self):
        """
        Called when a form of a survey using this workflow is created, deleted or updated.
        Not called for form field updates.
        """

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
            response.set_dimension_values(self.survey.cached_default_response_dimensions, cache=cache)

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
        override_dimensions: bool = False,
    ) -> Involvement | None:
        """
        If the response ought to result in Involvement, create it.
        """
        from kompassi.involvement.models.involvement import Involvement

        if not response.survey.registry:
            return None

        return Involvement.from_survey_response(
            response=response,
            old_version=old_version,
            cache=cache,
            override_dimensions=override_dimensions,
        )

    def ensure_survey_to_badge(self, response: Response):
        """
        Invoke Survey to Badge (STB) for new responses.
        See https://outline.con2.fi/doc/survey-to-badge-stb-mxK1UW6hAn

        TODO Deprecate in favor of Involvement
        """
        from kompassi.badges.models.badge import Badge
        from kompassi.badges.models.survey_to_badge import SurveyToBadgeMapping

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
            if self.is_allowed_for_user(subscriber, operation="query", field="responses")
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
        return response.superseded_by is None and self.is_allowed(request, operation="update", field="responses")

    def responses_can_be_deleted_by(self, request: HttpRequest) -> CanResponsesBeDeleted:
        if self.protect_responses:
            return CanResponsesBeDeleted.NO_PROTECTED

        if not self.is_allowed(request, operation="delete", field="responses"):
            return CanResponsesBeDeleted.NO_UNAUTHORIZED

        return CanResponsesBeDeleted.YES

    def response_can_be_deleted_by(
        self,
        response: Response,
        request: HttpRequest,
    ) -> CanResponsesBeDeleted:
        if not response.is_current_version:
            return CanResponsesBeDeleted.NO_OLD_VERSION

        return self.responses_can_be_deleted_by(request)

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
