import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from kompassi.core.middleware import RequestWithCache
from kompassi.core.utils.text_utils import normalize_whitespace
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.graphql_api.utils import resolve_local_datetime_field
from kompassi.involvement.graphql.profile_selected import SelectedProfileType
from kompassi.involvement.models.profile import Profile

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

        return Profile.from_person(person, response.survey.profile_field_selector)

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

        return Profile.from_person(person, response.survey.profile_field_selector)

    original_created_by = graphene.Field(
        SelectedProfileType,
        description=resolve_original_created_by.__doc__,
    )

    @staticmethod
    def resolve_cached_dimensions(
        response: Response,
        info,
        public_only: bool = True,
        key_dimensions_only: bool = False,
        list_filters_only: bool = False,
    ) -> CachedDimensions:
        """
        Returns a mapping of dimension slugs to lists of value slugs.

        Using `cachedDimensions` is faster than `dimensions` as it requires less joins and database queries.
        The difference is negligible for a response, but when operating on the plural resolver `responses`,
        the performance difference can be significant.

        By default, returns only public dimensions. If `publicOnly` is set to `false`,
        both public and internal dimensions will be returned. In this case, authentication is required.

        To limit the returned dimensions to key dimensions, set `keyDimensionsOnly: true` (default is `false`).
        To limit the returned dimensions to list filters, set `listFiltersOnly: true` (default is `false`).
        """

        request: RequestWithCache = info.context
        cache = request.kompassi_cache
        dimension_cache = cache.for_universe(response.survey.universe).dimension_cache
        cached_dimensions = response.cached_dimensions

        if public_only:
            cached_dimensions = {
                k: v for (k, v) in cached_dimensions.items() if dimension_cache.dimensions[k].is_public
            }
        else:
            cache.check_permission(
                instance=response,
                app=response.survey.universe.app_name,
            )

        if key_dimensions_only:
            cached_dimensions = {
                k: v for (k, v) in cached_dimensions.items() if dimension_cache.dimensions[k].is_key_dimension
            }

        if list_filters_only:
            cached_dimensions = {
                k: v for (k, v) in cached_dimensions.items() if dimension_cache.dimensions[k].is_list_filter
            }

        return cached_dimensions

    cached_dimensions = graphene.Field(
        GenericScalar,
        public_only=graphene.Boolean(default_value=True),
        key_dimensions_only=graphene.Boolean(default_value=False),
        list_filters_only=graphene.Boolean(default_value=False),
        description=normalize_whitespace(resolve_cached_dimensions.__doc__ or ""),
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

    @staticmethod
    def resolve_can_accept(
        response: Response,
        info,
    ):
        """
        Returns whether the response can be accepted by the user as an administrator.
        Not all survey workflows have the notion of accepting a response, in which case
        this field will always return False.
        """
        return response.survey.workflow.response_can_be_accepted_by(response, info.context)

    can_accept = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_can_accept.__doc__ or ""),
    )

    @staticmethod
    def resolve_can_cancel(
        response: Response,
        info,
    ):
        """
        Returns whether the response can be cancelled by the user.
        Not all survey workflows have the notion of cancelling a response, in which case
        this field will always return False.
        """
        return response.survey.workflow.response_can_be_cancelled_by(response, info.context)

    can_cancel = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_can_cancel.__doc__ or ""),
    )

    @staticmethod
    def resolve_can_delete(
        response: Response,
        info,
    ):
        return response.survey.workflow.response_can_be_deleted_by(response, info.context)

    can_delete = graphene.NonNull(
        graphene.Boolean,
        description="Whether the response can be deleted by the user.",
    )

    class Meta:
        model = Response
        fields = (
            "id",
            "form_data",
            "revision_created_at",
            "sequence_number",
        )
