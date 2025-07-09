import graphene
from graphene.types.generic import GenericScalar
from graphene_pydantic import PydanticObjectType

from graphql_api.language import DEFAULT_LANGUAGE
from graphql_api.utils import resolve_localized_field

from ..models.annotations import AnnotationSchemoid


class AnnotationSchemoidType(PydanticObjectType):
    class Meta:
        model = AnnotationSchemoid
        only_fields = (
            "slug",
            "type",
            "is_public",
            "is_shown_in_detail",
            "is_computed",
        )

    resolve_title = resolve_localized_field("title")
    title = graphene.NonNull(graphene.String, lang=graphene.String())

    resolve_description = resolve_localized_field("description")
    description = graphene.NonNull(graphene.String, lang=graphene.String())


class ProgramAnnotationType(graphene.ObjectType):
    annotation = graphene.NonNull(AnnotationSchemoidType)

    def resolve_value(self, info, lang: str = DEFAULT_LANGUAGE):
        """
        TODO: Implement localization for annotation values.
        """
        return self.value

    value = graphene.Field(GenericScalar, lang=graphene.String())
