import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from graphql_api.language import DEFAULT_LANGUAGE
from graphql_api.utils import resolve_localized_field

from ..models.annotation import Annotation, EventAnnotation
from ..models.enums import AnnotationDataType

AnnotationDataTypeType = graphene.Enum.from_enum(AnnotationDataType)


class AnnotationType(DjangoObjectType):
    class Meta:
        model = Annotation
        fields = (
            "slug",
            "is_public",
            "is_shown_in_detail",
            "is_computed",
            "is_applicable_to_program_items",
            "is_applicable_to_schedule_items",
        )

    type = graphene.NonNull(AnnotationDataTypeType)

    resolve_title = resolve_localized_field("title")
    title = graphene.NonNull(graphene.String, lang=graphene.String())

    resolve_description = resolve_localized_field("description")
    description = graphene.NonNull(graphene.String, lang=graphene.String())
    is_internal = graphene.NonNull(graphene.Boolean)


class EventAnnotationType(DjangoObjectType):
    class Meta:
        model = EventAnnotation
        fields = (
            "meta",
            "annotation",
            "is_active",
            "program_form_fields",
        )


class ProgramAnnotationType(graphene.ObjectType):
    annotation = graphene.NonNull(AnnotationType)

    def resolve_value(self, info, lang: str = DEFAULT_LANGUAGE):
        """
        TODO: Implement localization for annotation values.
        """
        return self.value

    value = graphene.Field(GenericScalar, lang=graphene.String())
