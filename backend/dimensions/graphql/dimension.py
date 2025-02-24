import graphene
from django.http import HttpRequest
from graphene_django import DjangoObjectType

from dimensions.models.dimension import Dimension
from graphql_api.language import DEFAULT_LANGUAGE
from graphql_api.utils import resolve_localized_field_getattr

from .dimension_value import DimensionValueType


# NOTE: names may not clash with program_v2.DimensionType and program_v2.DimensionValueType
# TODO unify these
class DimensionType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field_getattr("title")

    @staticmethod
    def resolve_can_remove(dimension: Dimension, info):
        request: HttpRequest = info.context
        return dimension.can_be_deleted_by(request)

    can_remove = graphene.NonNull(graphene.Boolean)

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

    class Meta:
        model = Dimension
        fields = ("slug", "values", "is_key_dimension", "is_multi_value")
