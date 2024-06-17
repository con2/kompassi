import graphene
from graphene.types.generic import GenericScalar
from graphene_pydantic import PydanticObjectType

from graphql_api.utils import resolve_localized_field

from ..models.annotations import AnnotationSchemoid


class AnnotationSchemoidType(PydanticObjectType):
    class Meta:
        model = AnnotationSchemoid
        only_fields = ("slug", "type", "is_public", "is_shown_in_detail")

    resolve_title = resolve_localized_field("title")
    title = graphene.NonNull(graphene.String, lang=graphene.String())

    resolve_description = resolve_localized_field("description")
    description = graphene.NonNull(graphene.String, lang=graphene.String())


class ProgramAnnotationType(graphene.ObjectType):
    annotation = graphene.NonNull(AnnotationSchemoidType)
    value = graphene.Field(GenericScalar)
