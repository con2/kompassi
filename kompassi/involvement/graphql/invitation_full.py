import graphene

from kompassi.core.graphql.user_limited import LimitedUserType
from kompassi.forms.graphql.survey_full import FullSurveyType
from kompassi.graphql_api.utils import resolve_local_datetime_field
from kompassi.program_v2.graphql.program_limited import LimitedProgramType

from ..models.invitation import Invitation
from .invitation_limited import LimitedInvitationType


class FullInvitationType(LimitedInvitationType):
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

    survey = graphene.Field(FullSurveyType)
    program = graphene.Field(LimitedProgramType)
    created_by = graphene.Field(LimitedUserType)

    resolve_used_at = resolve_local_datetime_field("used_at")
