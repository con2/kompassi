import graphene
from graphene_django import DjangoObjectType

from kompassi.dimensions.models.dimension import Dimension
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.graphql_api.utils import resolve_localized_field_getattr

from .dimension_value import DimensionValueType


class FullDimensionType(DjangoObjectType):
    class Meta:
        model = Dimension
        fields = (
            "slug",
            "values",
            "is_public",
            "is_key_dimension",
            "is_multi_value",
            "is_list_filter",
            "is_shown_in_detail",
            "is_negative_selection",
            "is_technical",
            "value_ordering",
            # NOTE SUPPORTED_LANGUAGES
            "title_en",
            "title_fi",
            "title_sv",
        )

    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field_getattr("title")

    @staticmethod
    def resolve_can_remove(dimension: Dimension, info):
        return dimension.can_be_deleted_by(info.context)

    can_remove = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_can_add_values(dimension: Dimension, info):
        return dimension.can_values_be_created_by(info.context)

    can_add_values = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_values(
        dimension: Dimension,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ):
        """
        Get values of a dimension, ordered according to the dimension's `value_ordering`.
        NOTE: In order to get the ordering in the correct language, the language needs to be provided.
        """
        return dimension.get_values(lang)

    values = graphene.NonNull(
        graphene.List(graphene.NonNull(DimensionValueType)),
        lang=graphene.String(),
    )

    @staticmethod
    def resolve_is_shown_to_subject(dimension: Dimension, info):
        return dimension.is_public and dimension.is_key_dimension

    is_shown_to_subject = graphene.NonNull(graphene.Boolean)
