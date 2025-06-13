from enum import Enum

import graphene
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from access.cbac import graphql_check_model, is_graphql_allowed_for_model
from core.utils import get_objects_within_period, normalize_whitespace

from ..models.enums import SurveyApp
from ..models.meta import FormsEventMeta, FormsProfileMeta
from ..models.response import Response
from ..models.survey import Survey, SurveyPurpose
from .enums import SurveyAppType, SurveyPurposeType
from .response_profile import ProfileResponseType
from .survey_full import FullSurveyType

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class SurveyRelation(Enum):
    SUBSCRIBED = "SUBSCRIBED"
    ACCESSIBLE = "ACCESSIBLE"


class FormsEventMetaType(graphene.ObjectType):
    surveys = graphene.NonNull(
        graphene.List(
            graphene.NonNull(FullSurveyType),
        ),
        include_inactive=graphene.Boolean(),
        app=graphene.NonNull(SurveyAppType),
        purpose=graphene.List(graphene.NonNull(SurveyPurposeType)),
    )

    @staticmethod
    def resolve_surveys(
        meta: FormsEventMeta,
        info,
        app: SurveyApp,
        include_inactive: bool = False,
        purpose: list[SurveyPurpose] | None = None,
    ):
        """
        By default only returns active surveys, ie. surveys with `activeFrom` in the past and
        `activeUntil` either unset or in the future.

        To get inactive surveys as well, pass `includeInactive: true` (authorization required).

        By default only returns surveys with `purpose: DEFAULT`. To get special purpose surveys,
        specify `purposes`.

        NOTE: `app` does not currently accept `null` (for surveys of all apps)
        because access control is performed app by app (`app` CBAC claim).
        Until TODO(#324), you can as a workaround do something like
        `surveys: surveys(app: FORMS), programForms: surveys(app: PROGRAM_V2)`.
        """
        qs = Survey.objects.filter(event=meta.event, app_name=app.value)

        if purpose:
            qs = qs.filter(purpose_slug__in=[SurveyPurpose(p).value for p in purpose])
        else:
            qs = qs.filter(purpose_slug=SurveyPurpose.DEFAULT.value)

        if include_inactive:
            graphql_check_model(Survey, meta.event.scope, info, app=app)
        else:
            qs = get_objects_within_period(qs)

        return qs.order_by("slug")

    survey = graphene.Field(
        FullSurveyType,
        slug=graphene.String(required=True),
        app=graphene.Argument(SurveyAppType),
        purpose=graphene.Argument(SurveyPurposeType),
    )

    @staticmethod
    def resolve_survey(
        meta: FormsEventMeta,
        info,
        slug: str,
        app: SurveyApp | None = None,
        purpose: SurveyPurpose | None = None,
    ):
        """
        Pass `app: null` to include surveys of all apps (default: `FORMS`).
        """
        qs = Survey.objects.filter(event=meta.event, slug=slug)

        if app:
            qs = qs.filter(app_name=app.value)

        if purpose:
            qs = qs.filter(purpose_slug=purpose.value)

        return qs.first()

        # TODO Rethink this. With this check, we cannot supply a reasonable
        # "Survey is not active" error message.
        # survey = qs.first()
        # if survey and not survey.is_active:
        #     graphql_check_instance(survey, info, app=survey.app)
        # return survey


class FormsProfileMetaType(graphene.ObjectType):
    @staticmethod
    def resolve_responses(meta: FormsProfileMeta, info):
        """
        Returns all responses submitted by the current user.
        """
        if info.context.user != meta.person.user:
            raise SuspiciousOperation("User mismatch")
        return Response.objects.filter(
            revision_created_by=meta.person.user,
            superseded_by=None,
        ).order_by("-revision_created_at")

    responses = graphene.NonNull(
        graphene.List(
            graphene.NonNull(ProfileResponseType),
        ),
        description=normalize_whitespace(resolve_responses.__doc__ or ""),
    )

    @staticmethod
    def resolve_response(meta: FormsProfileMeta, info, id: str):
        """
        Returns a single response submitted by the current user.
        """
        if info.context.user != meta.person.user:
            raise SuspiciousOperation("User mismatch")
        return Response.objects.get(revision_created_by=meta.person.user, id=id)

    response = graphene.Field(
        ProfileResponseType,
        id=graphene.String(required=True),
        description=normalize_whitespace(resolve_response.__doc__ or ""),
    )

    @staticmethod
    def resolve_surveys(
        meta: FormsProfileMeta,
        info,
        event_slug: str | None = None,
        relation: SurveyRelation = SurveyRelation.ACCESSIBLE,
    ):
        """
        Returns all surveys accessible by the current user.
        To limit to surveys subscribed to, specify `relation: SUBSCRIBED`.
        To limit by event, specify `eventSlug: $eventSlug`.
        """
        if info.context.user != meta.person.user:
            raise SuspiciousOperation("User mismatch")

        surveys = Survey.objects.all()
        if relation == SurveyRelation.SUBSCRIBED:
            surveys = surveys.filter(subscribers=meta.person.user)
        if event_slug:
            surveys = surveys.filter(event__slug=event_slug)

        # TODO(#324)
        return [
            survey
            for survey in surveys
            if is_graphql_allowed_for_model(
                meta.person.user,
                instance=survey,  # type: ignore
                operation="query",
                field="self",
                app=survey.app_name,  # TODO(#574) check this
            )
        ]

    surveys = graphene.NonNull(
        graphene.List(
            graphene.NonNull(FullSurveyType),
        ),
        event_slug=graphene.String(),
        relation=graphene.Argument(graphene.Enum.from_enum(SurveyRelation)),
        description=normalize_whitespace(resolve_surveys.__doc__ or ""),
    )
