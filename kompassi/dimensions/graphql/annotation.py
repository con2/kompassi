import graphene
from graphene_django import DjangoObjectType

from kompassi.graphql_api.utils import resolve_localized_field_getattr

from ..models.annotation import Annotation
from ..models.enums import AnnotationDataType

AnnotationDataTypeType = graphene.Enum.from_enum(AnnotationDataType)


class AnnotationType(DjangoObjectType):
    class Meta:
        model = Annotation
        fields = ("slug",)

    type = graphene.NonNull(AnnotationDataTypeType)

    resolve_title = resolve_localized_field_getattr("title")
    title = graphene.NonNull(graphene.String, lang=graphene.String())

    resolve_description = resolve_localized_field_getattr("description")
    description = graphene.NonNull(graphene.String, lang=graphene.String())

    is_internal = graphene.NonNull(graphene.Boolean)
    is_public = graphene.NonNull(graphene.Boolean)
    is_shown_in_detail = graphene.NonNull(graphene.Boolean)
    is_computed = graphene.NonNull(graphene.Boolean)
    is_applicable_to_program_items = graphene.NonNull(graphene.Boolean)
    is_applicable_to_schedule_items = graphene.NonNull(graphene.Boolean)
