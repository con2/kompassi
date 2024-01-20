import graphene
from django.contrib.auth.models import User
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from core.graphql.user import LimitedUserType
from core.utils.text_utils import normalize_whitespace

from ..models.response import Response
from .dimension import ResponseDimensionValueType
from .form import FormType


class LimitedResponseType(DjangoObjectType):
    @staticmethod
    def resolve_values(
        response: Response,
        info,
        key_fields_only: bool = False,
    ):
        values = response.values

        if key_fields_only:
            survey = response.form.survey
            key_fields = survey.key_fields if survey else []
            values = {k: v for k, v in values.items() if k in key_fields}

        return values

    values = graphene.Field(
        GenericScalar,
        key_fields_only=graphene.Boolean(
            description=(
                "If the response is related to a survey, only return values of fields "
                "marked key fields in the survey. Note that setting keyFieldsOnly for a "
                "response not related to a survey will result in an empty list."
            ),
        ),
    )

    @staticmethod
    def resolve_language(response: Response, info):
        return response.form.language

    language = graphene.Field(
        graphene.NonNull(graphene.String),
        description="Language code of the form used to submit this response.",
    )

    @staticmethod
    def resolve_created_by(response: Response, info) -> User | None:
        """
        Returns the user who submitted the response. If response is to an anonymous survey,
        this information will not be available.
        """
        if (survey := response.form.survey) and survey.anonymity in ("hard", "soft"):
            return None

        return response.created_by

    created_by = graphene.Field(
        LimitedUserType,
        description=resolve_created_by.__doc__,
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
        """
        cached_dimensions = response.cached_dimensions

        if key_dimensions_only:
            survey = response.survey
            if survey is None:
                return {}

            dimensions_by_slug = {dimension.slug: dimension for dimension in survey.dimensions.all()}

            return {
                k: v
                for k, v in cached_dimensions.items()
                if (dimension := dimensions_by_slug.get(k)) and dimension.is_key_dimension
            }

        return cached_dimensions

    cached_dimensions = graphene.Field(
        GenericScalar,
        description=normalize_whitespace(resolve_cached_dimensions.__doc__ or ""),
        key_dimensions_only=graphene.Boolean(),
    )

    class Meta:
        model = Response
        fields = ("id", "form_data", "created_at")


class FullResponseType(LimitedResponseType):
    @staticmethod
    def resolve_form(parent: Response, info):
        return parent.form

    form = graphene.Field(graphene.NonNull(FormType))

    @staticmethod
    def resolve_dimensions(parent: Response, info, key_dimensions_only: bool = False):
        qs = parent.dimensions.all()

        if key_dimensions_only:
            qs = qs.filter(dimension__is_key_dimension=True)

        return qs

    dimensions = graphene.List(
        graphene.NonNull(ResponseDimensionValueType),
        key_dimensions_only=graphene.Boolean(),
    )

    class Meta:
        model = Response
        fields = (
            "id",
            "form_data",
            "created_at",
        )
