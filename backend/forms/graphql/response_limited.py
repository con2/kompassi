import graphene
from django.contrib.auth.models import User
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from core.graphql.user import LimitedUserType
from core.utils.text_utils import normalize_whitespace
from graphql_api.utils import resolve_local_datetime_field

from ..models.response import Response


class LimitedResponseType(DjangoObjectType):
    @staticmethod
    def resolve_values(
        response: Response,
        info,
        key_fields_only: bool = False,
    ):
        if key_fields_only:
            return response.cached_key_fields
        else:
            # TODO discards warnings :(
            return response.get_processed_form_data()[0]

    values = graphene.Field(
        GenericScalar,
        key_fields_only=graphene.Boolean(
            description="Only return values of fields marked key fields in the survey.",
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
        if (survey := response.form.survey) and survey.anonymity in ("HARD", "SOFT"):
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
            key_dimension_slugs = response.dimensions.filter(
                value__dimension__slug__in=cached_dimensions.keys(),
                value__dimension__is_key_dimension=True,
            ).values_list("value__dimension__slug", flat=True)

            return {k: v for k, v in cached_dimensions.items() if k in key_dimension_slugs}

        return cached_dimensions

    cached_dimensions = graphene.Field(
        GenericScalar,
        description=normalize_whitespace(resolve_cached_dimensions.__doc__ or ""),
        key_dimensions_only=graphene.Boolean(),
    )

    resolve_created_at = resolve_local_datetime_field("created_at")

    class Meta:
        model = Response
        fields = (
            "id",
            "form_data",
            "created_at",
            "sequence_number",
        )
