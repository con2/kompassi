import graphene
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from access.cbac import graphql_check_instance, graphql_check_model, is_graphql_allowed_for_model
from core.utils import get_objects_within_period, normalize_whitespace

from ..models.enums import SurveyApp
from ..models.meta import FormsEventMeta, FormsProfileMeta
from ..models.response import Response
from ..models.survey import Survey
from .response import ProfileResponseType
from .survey_full import SurveyType

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


SurveyAppType = graphene.Enum.from_enum(SurveyApp)


class FormsEventMetaType(graphene.ObjectType):
    surveys = graphene.List(
        graphene.NonNull(SurveyType),
        include_inactive=graphene.Boolean(),
        app=graphene.NonNull(SurveyAppType),
    )

    @staticmethod
    def resolve_surveys(
        meta: FormsEventMeta,
        info,
        app: SurveyApp,
        include_inactive: bool = False,
    ):
        """
        By default only returns active surveys, ie. surveys with `activeFrom` in the past and
        `activeUntil` either unset or in the future.

        To get inactive surveys as well, pass `includeInactive: true` (authorization required).

        NOTE: `app` does not currently accept `null` (for surveys of all apps)
        because access control is performed app by app (`app` CBAC claim).
        Until TODO(#324), you can as a workaround do something like
        `surveys: surveys(app: FORMS), programForms: surveys(app: PROGRAM_V2)`.
        """
        qs = Survey.objects.filter(event=meta.event, app=app.value)

        if include_inactive:
            graphql_check_model(Survey, meta.event.scope, info, app=app.value)
        else:
            qs = get_objects_within_period(Survey, event=meta.event)

        return qs

    survey = graphene.Field(
        SurveyType,
        slug=graphene.String(required=True),
        app=graphene.Argument(SurveyAppType),
    )

    @staticmethod
    def resolve_survey(
        meta: FormsEventMeta,
        info,
        slug: str,
        app: SurveyApp | None = None,
    ):
        """
        Pass `app: null` to include surveys of all apps (default: `FORMS`).
        """
        qs = Survey.objects.filter(event=meta.event, slug=slug)

        if app:
            qs = qs.filter(app=app)

        survey = qs.first()

        if survey and not survey.is_active:
            graphql_check_instance(survey, info, app=survey.app)

        return survey


class FormsProfileMetaType(graphene.ObjectType):
    @staticmethod
    def resolve_responses(meta: FormsProfileMeta, info):
        """
        Returns all responses submitted by the current user.
        """
        if info.context.user != meta.person.user:
            raise SuspiciousOperation("User mismatch")
        return Response.objects.filter(created_by=meta.person.user).order_by("-created_at")

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
        return Response.objects.get(created_by=meta.person.user, id=id)

    response = graphene.Field(
        ProfileResponseType,
        id=graphene.String(required=True),
        description=normalize_whitespace(resolve_response.__doc__ or ""),
    )

    @staticmethod
    def resolve_surveys(meta: FormsProfileMeta, info, event_slug: str | None = None):
        """
        Returns all surveys subscribed to by the current user.
        """
        if info.context.user != meta.person.user:
            raise SuspiciousOperation("User mismatch")

        surveys = Survey.objects.filter(subscribers=meta.person.user)

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
                app=survey.app,  # TODO(#574) check this
            )
        ]

    surveys = graphene.NonNull(
        graphene.List(
            graphene.NonNull(SurveyType),
        ),
        event_slug=graphene.String(),
        description=normalize_whitespace(resolve_surveys.__doc__ or ""),
    )
