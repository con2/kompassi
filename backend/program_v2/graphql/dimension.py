import graphene
from graphene_django import DjangoObjectType

from graphql_api.language import DEFAULT_LANGUAGE
from graphql_api.utils import resolve_localized_field

from ..models.dimension import Dimension, DimensionValue, ProgramDimensionValue

# class ValueOrdering(graphene.Enum):
#     DEFAULT = "default"
#     MANUAL = "manual"
#     SLUG = "slug"
#     TITLE = "title"


class DimensionValueType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field("title")

    class Meta:
        model = DimensionValue
        fields = (
            "slug",
            "color",
        )


class DimensionType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field("title")

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

    class Meta:
        model = Dimension
        fields = (
            "slug",
            "is_multi_value",
            "is_list_filter",
            "is_shown_in_detail",
            "is_negative_selection",
        )


class ProgramDimensionValueType(DjangoObjectType):
    class Meta:
        model = ProgramDimensionValue
        fields = ("dimension", "value")
