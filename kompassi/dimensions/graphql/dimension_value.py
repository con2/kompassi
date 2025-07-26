import graphene
from graphene_django import DjangoObjectType

from kompassi.dimensions.models.dimension_value import DimensionValue
from kompassi.graphql_api.utils import resolve_localized_field_getattr


class DimensionValueType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field_getattr("title")

    @staticmethod
    def resolve_can_remove(value: DimensionValue, info):
        return value.can_be_deleted_by(info.context)

    can_remove = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_can_edit(value: DimensionValue, info):
        return value.can_be_updated_by(info.context)

    can_edit = graphene.NonNull(graphene.Boolean)

    class Meta:
        model = DimensionValue
        fields = (
            "slug",
            "color",
            "is_technical",
            "is_subject_locked",
            # NOTE SUPPORTED_LANGUAGES
            "title_en",
            "title_fi",
            "title_sv",
        )
