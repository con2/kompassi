import graphene
import graphene_django
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.forms.graphql.survey_limited import LimitedSurveyType
from kompassi.graphql_api.utils import resolve_local_datetime_field

from ..models.invitation import Invitation


class LimitedInvitationType(graphene_django.DjangoObjectType):
    class Meta:
        model = Invitation
        fields = (
            "id",
            "survey",
            "language",
            "cached_dimensions",
        )

    survey = graphene.Field(LimitedSurveyType)

    @staticmethod
    def resolve_is_used(invitation: Invitation, info) -> bool:
        return invitation.used_at is not None

    is_used = graphene.NonNull(graphene.Boolean)

    resolve_created_at = resolve_local_datetime_field("created_at")
    created_at = graphene.NonNull(graphene.DateTime)
    cached_dimensions = GenericScalar()

    @staticmethod
    def resolve_email(invitation: Invitation, info) -> str:
        graphql_check_instance(
            invitation,
            info,
            field="email",
            app=invitation.app.app_name,
        )

        return invitation.email

    email = graphene.NonNull(graphene.String)
