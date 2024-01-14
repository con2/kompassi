import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from ..models.response import Response
from .form import FormType


class LimitedResponseType(DjangoObjectType):
    @staticmethod
    def resolve_values(
        response: Response,
        info,
        key_fields_only: bool = False,
    ):
        values = response.values

        if key_fields_only:
            survey = response.form.survey
            key_fields = survey.key_fields if survey else []
            values = {k: v for k, v in values.items() if k in key_fields}

        return values

    values = graphene.Field(
        GenericScalar,
        key_fields_only=graphene.Boolean(
            description=(
                "If the response is related to a survey, only return values of fields "
                "marked key fields in the survey. Note that setting keyFieldsOnly for a "
                "response not related to a survey will result in an empty list."
            ),
        ),
    )

    @staticmethod
    def resolve_language(response: Response, info):
        return response.form.language

    language = graphene.Field(
        graphene.NonNull(graphene.String),
        description="Language code of the form used to submit this response.",
    )

    class Meta:
        model = Response
        fields = ("id", "form_data", "created_at")


class FullResponseType(LimitedResponseType):
    form = graphene.Field(graphene.NonNull(FormType))

    @staticmethod
    def resolve_form(parent: Response, info):
        return parent.form

    class Meta:
        model = Response
        fields = ("id", "form_data", "created_at")
