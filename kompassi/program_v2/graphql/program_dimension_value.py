import graphene
from graphene_django import DjangoObjectType

from kompassi.dimensions.graphql.dimension_full import FullDimensionType

from ..models.program_dimension_value import ProgramDimensionValue


class ProgramDimensionValueType(DjangoObjectType):
    class Meta:
        model = ProgramDimensionValue
        fields = ("value",)

    dimension = graphene.NonNull(FullDimensionType)

    @staticmethod
    def resolve_dimension(pdv: ProgramDimensionValue, info):
        return pdv.value.dimension
