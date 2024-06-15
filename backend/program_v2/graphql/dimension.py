import graphene
from graphene_django import DjangoObjectType

from graphql_api.language import DEFAULT_LANGUAGE
from graphql_api.utils import get_message_in_language, resolve_localized_field

from ..models.dimension import Dimension, DimensionValue, ProgramDimensionValue, ValueOrdering

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


ValueOrderingType = graphene.Enum.from_enum(ValueOrdering)


class DimensionType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field("title")

    @staticmethod
    def resolve_values(
        dimension: Dimension,
        info,
        lang: str = DEFAULT_LANGUAGE,
        value_ordering: ValueOrdering | None = None,  # type: ignore
    ):
        """
        Get values of a dimension, ordered according to the dimension's `value_ordering`.
        NOTE: In order to get the ordering in the correct language, the language needs to be provided.
        """
        # XXX pyrekt does not rektify graphene.Enum

        dimensions = dimension.values.all()
        value_ordering_fmh = dimension.value_ordering if value_ordering is None else value_ordering.value

        print("value_ordering_fmh", value_ordering_fmh)

        match value_ordering_fmh:
            case "manual":
                dimensions = dimensions.order_by("order")
            case "slug":
                dimensions = dimensions.order_by("slug")
            case "title":

                def key_func(value: DimensionValue) -> str:
                    return get_message_in_language(value.title, lang) or value.slug

                dimensions = sorted(dimensions, key=key_func)

        return dimensions

    values = graphene.NonNull(
        graphene.List(graphene.NonNull(DimensionValueType)),
        lang=graphene.String(),
        value_ordering=ValueOrderingType(),
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
