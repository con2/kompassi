import graphene
from django.conf import settings
from graphene_django import DjangoObjectType

from ..models.survey import Survey

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class LimitedSurveyType(DjangoObjectType):
    title = graphene.Field(graphene.String, lang=graphene.String())

    @staticmethod
    def resolve_title(parent: Survey, info, lang: str = DEFAULT_LANGUAGE):
        return form.title if (form := parent.get_form(lang)) else None

    is_active = graphene.Field(graphene.NonNull(graphene.Boolean))

    @staticmethod
    def resolve_is_active(parent: Survey, info) -> bool:
        return parent.is_active

    class Meta:
        model = Survey
        fields = (
            "slug",
            "active_from",
            "active_until",
            "login_required",
            "anonymity",
            "max_responses_per_user",
        )
