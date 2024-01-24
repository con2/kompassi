import graphene
from graphene_django import DjangoObjectType

from graphql_api.utils import resolve_localized_field

from ..models import Dimension, DimensionValue, ResponseDimensionValue


# NOTE: names may not clash with program_v2.DimensionType and program_v2.DimensionValueType
class SurveyDimensionType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field("title")

    class Meta:
        model = Dimension
        fields = ("slug", "values", "is_key_dimension", "is_multi_value")


class SurveyDimensionValueType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field("title")

    class Meta:
        model = DimensionValue
        fields = ("slug", "color")


class ResponseDimensionValueType(DjangoObjectType):
    class Meta:
        model = ResponseDimensionValue
        fields = ("dimension", "value")
