import graphene
from django.http import HttpRequest
from graphene_django import DjangoObjectType

from dimensions.models.dimension_value import DimensionValue
from graphql_api.utils import resolve_localized_field_getattr


class SurveyDimensionValueType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field_getattr("title")

    @staticmethod
    def resolve_can_remove(value: DimensionValue, info):
        request: HttpRequest = info.context
        return value.can_be_deleted_by(request)

    can_remove = graphene.NonNull(graphene.Boolean)

    class Meta:
        model = DimensionValue
        fields = ("slug", "color", "is_initial")
