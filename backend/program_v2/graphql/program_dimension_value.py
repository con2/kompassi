import graphene
from graphene_django import DjangoObjectType

from dimensions.graphql.dimension import DimensionType

from ..models.program_dimension_value import ProgramDimensionValue


class ProgramDimensionValueType(DjangoObjectType):
    class Meta:
        model = ProgramDimensionValue
        fields = ("value",)

    dimension = graphene.NonNull(DimensionType)

    @staticmethod
    def resolve_dimension(pdv: ProgramDimensionValue, info):
        return pdv.value.dimension
