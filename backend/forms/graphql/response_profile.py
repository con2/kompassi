import graphene
from graphene.types.generic import GenericScalar

from core.utils.text_utils import normalize_whitespace

from ..models.response import Response
from .form import FormType
from .response_dimension_value import ResponseDimensionValueType
from .response_limited import LimitedResponseType


class ProfileResponseType(LimitedResponseType):
    @staticmethod
    def resolve_form(parent: Response, info):
        return parent.form

    form = graphene.Field(graphene.NonNull(FormType))

    @staticmethod
    def resolve_dimensions(response: Response, info, key_dimensions_only: bool = False):
        """
        The respondent will only see values of dimensions that are designated as
        being shown to the respondent.
        """
        qs = response.dimensions.filter(value__dimension__is_public=True)

        if key_dimensions_only:
            qs = qs.filter(value__dimension__is_key_dimension=True)

        return qs.order_by("value__dimension__order", "value__order", "value__slug")

    dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(ResponseDimensionValueType)),
        key_dimensions_only=graphene.Boolean(),
    )

    @staticmethod
    def resolve_cached_dimensions(response: Response, info, key_dimensions_only: bool = False):
        """
        Returns the dimensions of the response as
        a dict of dimension slug -> list of dimension value slugs. If the response
        is not related to a survey, there will be no dimensions and an empty dict
        will always be returned.

        Using this field is more efficient than querying the dimensions field
        on the response, as the dimensions are cached on the response object.

        The respondent will only see values of dimensions that are designated as
        being shown to the respondent.
        """
        cached_dimensions = response.cached_dimensions

        included_dimensions = response.dimensions.filter(
            value__dimension__slug__in=cached_dimensions.keys(),
            value__dimension__is_shown_to_subject=True,
        )

        if key_dimensions_only:
            included_dimensions = included_dimensions.filter(value__dimension__is_key_dimension=True)

        included_dimension_slugs = response.dimensions.values_list("value__dimension__slug", flat=True)

        return {k: v for k, v in cached_dimensions.items() if k in included_dimension_slugs}

    cached_dimensions = graphene.Field(
        GenericScalar,
        description=normalize_whitespace(resolve_cached_dimensions.__doc__ or ""),
        key_dimensions_only=graphene.Boolean(),
    )

    @staticmethod
    def resolve_old_versions(response: Response, info):
        return response.old_versions.all()

    old_versions = graphene.NonNull(graphene.List(graphene.NonNull(LimitedResponseType)))

    superseded_by = graphene.Field(
        LimitedResponseType,
        description="If this response is an old version, this field will point to the current version.",
    )

    class Meta:
        model = Response
        fields = (
            "id",
            "form_data",
            "superseded_by",
            "revision_created_at",
        )
