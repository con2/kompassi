import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from core.utils.text_utils import normalize_whitespace
from graphql_api.utils import resolve_local_datetime_field
from involvement.graphql.profile_selected import SelectedProfileType
from involvement.models.profile import Profile

from ..models.enums import EditMode
from ..models.response import Response
from .enums import EditModeType


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
    def resolve_revision_created_by(response: Response, info) -> Profile | None:
        """
        Returns the user who submitted this version of the response.
        If response is to an anonymous survey, this information will not be available.
        """

        if (survey := response.form.survey) and survey.anonymity in ("HARD", "SOFT"):
            return None

        if not response.revision_created_by:
            return None

        person = response.revision_created_by.person
        if not person:
            return None

        return response.survey.profile_field_selector.select(person)

    revision_created_by = graphene.Field(
        SelectedProfileType,
        description=resolve_revision_created_by.__doc__,
    )

    @staticmethod
    def resolve_original_created_by(response: Response, info) -> Profile | None:
        """
        Returns the user who originally submitted this response.
        If response is to an anonymous survey, this information will not be available.
        """

        if (survey := response.form.survey) and survey.anonymity in ("HARD", "SOFT"):
            return None

        if not response.original_created_by:
            return None

        person = response.original_created_by.person  # type: ignore
        if not person:
            return None

        return response.survey.profile_field_selector.select(person)

    original_created_by = graphene.Field(
        SelectedProfileType,
        description=resolve_original_created_by.__doc__,
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
        graphene.NonNull(GenericScalar),
        description=normalize_whitespace(resolve_cached_dimensions.__doc__ or ""),
        key_dimensions_only=graphene.Boolean(),
    )

    resolve_original_created_at = resolve_local_datetime_field("original_created_at")
    original_created_at = graphene.Field(
        graphene.NonNull(graphene.DateTime),
        description="The date and time when the response was originally created.",
    )

    resolve_revision_created_at = resolve_local_datetime_field("revision_created_at")

    @staticmethod
    def resolve_can_edit(
        response: Response,
        info,
        mode: EditMode = EditMode.ADMIN,
    ):
        """
        Returns whether the response can be edited by the user in the given edit mode.

        The edit mode can be either ADMIN (default) or OWN.
        ADMIN determines CBAC edit permissions, while OWN determines if the user
        is the owner of the response and editing it is allowed by the survey.
        """
        match mode:
            case EditMode.ADMIN:
                return response.survey.workflow.response_can_be_edited_by_admin(response, info.context)
            case EditMode.OWNER:
                return response.survey.workflow.response_can_be_edited_by_owner(response, info.context)
            case _:
                raise ValueError(f"Unknown edit mode: {mode}")

    can_edit = graphene.Field(
        graphene.NonNull(graphene.Boolean),
        description=normalize_whitespace(resolve_can_edit.__doc__ or ""),
        mode=graphene.Argument(EditModeType),
    )

    class Meta:
        model = Response
        fields = (
            "id",
            "form_data",
            "revision_created_at",
            "sequence_number",
        )
