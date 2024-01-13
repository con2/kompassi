import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from ..models.response import Response
from .form import FormType


class LimitedResponseType(DjangoObjectType):
    @staticmethod
    def resolve_values(response: Response, info):
        return response.values

    values = graphene.Field(GenericScalar)

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
