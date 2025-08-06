import graphene
from graphene.types.generic import GenericScalar

from kompassi.dimensions.graphql.annotation import AnnotationType
from kompassi.graphql_api.language import DEFAULT_LANGUAGE


class ProgramAnnotationType(graphene.ObjectType):
    annotation = graphene.NonNull(AnnotationType)

    def resolve_value(self, info, lang: str = DEFAULT_LANGUAGE):
        """
        TODO: Implement localization for annotation values.
        """
        return self.value

    value = graphene.Field(GenericScalar, lang=graphene.String())
