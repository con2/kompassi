import graphene
from graphene_django import DjangoObjectType

from kompassi.dimensions.graphql.dimension_full import FullDimensionType

from ..models.response_dimension_value import ResponseDimensionValue


class ResponseDimensionValueType(DjangoObjectType):
    class Meta:
        model = ResponseDimensionValue
        fields = ("value",)

    dimension = graphene.NonNull(FullDimensionType)

    @staticmethod
    def resolve_dimension(rdv: ResponseDimensionValue, info):
        return rdv.value.dimension
