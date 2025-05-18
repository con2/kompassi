import graphene
import graphene_django

from core.graphql.user_limited import LimitedUserType
from forms.graphql.survey_limited import LimitedSurveyType
from graphql_api.utils import resolve_local_datetime_field
from program_v2.graphql.program_limited import LimitedProgramType

from ..models.invitation import Invitation


class FullInvitationType(graphene_django.DjangoObjectType):
    class Meta:
        model = Invitation
        fields = (
            "id",
            "survey",
            "program",
            "used_at",
            "created_by",
            "language",
            "email",
        )

    survey = graphene.Field(LimitedSurveyType)
    program = graphene.Field(LimitedProgramType)
    created_by = graphene.Field(LimitedUserType)

    resolve_used_at = resolve_local_datetime_field("used_at")
