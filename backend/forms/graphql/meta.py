import graphene
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from access.cbac import graphql_check_access
from core.utils import get_objects_within_period, normalize_whitespace

from ..models.meta import FormsEventMeta, FormsProfileMeta
from ..models.response import Response
from ..models.survey import Survey
from .response import ProfileResponseType
from .survey import SurveyType

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class FormsEventMetaType(graphene.ObjectType):
    surveys = graphene.List(graphene.NonNull(SurveyType), include_inactive=graphene.Boolean())

    @staticmethod
    def resolve_surveys(meta: FormsEventMeta, info, include_inactive: bool = False):
        if include_inactive:
            graphql_check_access(meta, info, "surveys")
            qs = Survey.objects.filter(event=meta.event)
        else:
            qs = get_objects_within_period(Survey, event=meta.event)

        return qs

    survey = graphene.Field(SurveyType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_survey(meta: FormsEventMeta, info, slug: str):
        survey = Survey.objects.get(event=meta.event, slug=slug)

        if not survey.is_active:
            graphql_check_access(survey, info, "self")

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
    def resolve_response(meta: FormsProfileMeta, info, id: int):
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
