import graphene
from django.conf import settings
from django.http import HttpRequest
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.graphql.event_limited import LimitedEventType
from kompassi.core.utils import normalize_whitespace
from kompassi.dimensions.filters import DimensionFilters
from kompassi.dimensions.graphql.dimension_filter_input import DimensionFilterInput
from kompassi.dimensions.graphql.dimension_full import FullDimensionType

from ..models.form import Form
from ..models.survey import Survey
from ..utils.summarize_responses import summarize_responses
from .form import FormType
from .response_full import FullResponseType
from .response_limited import LimitedResponseType
from .survey_limited import LimitedSurveyType

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class FullSurveyType(LimitedSurveyType):
    @staticmethod
    def resolve_form(
        parent: Survey,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ) -> Form | None:
        """
        Will attempt to give the form in the requested language, falling back
        to another language if that language is not available.
        """
        return parent.get_form(lang)

    form = graphene.Field(
        FormType,
        lang=graphene.String(),
        description=normalize_whitespace(resolve_form.__doc__ or ""),
    )

    @staticmethod
    def resolve_fields(
        parent: Survey,
        info,
        lang: str = DEFAULT_LANGUAGE,
        key_fields_only: bool = False,
    ):
        """
        A survey's language versions may have differing fields. This field presents
        them combined as a single list of fields. If a language is specified,
        that language is used as the base for the combined fields. Order of fields
        not present in the base language is not guaranteed.
        """
        fields = parent.get_combined_fields(lang)

        if key_fields_only:
            fields = (field for field in fields if field.slug in parent.key_fields)

        return [
            field.model_dump(
                exclude_none=True,
                by_alias=True,
            )
            for field in fields
        ]

    fields = graphene.Field(
        GenericScalar,
        lang=graphene.String(),
        key_fields_only=graphene.Boolean(),
        description=normalize_whitespace(resolve_fields.__doc__ or ""),
    )

    @staticmethod
    def resolve_responses(
        survey: Survey,
        info,
        filters: list[DimensionFilterInput] | None = None,
    ):
        """
        Returns the responses to this survey regardless of language version used.
        Authorization required.
        """
        graphql_check_instance(survey, info, app=survey.app_name, field="responses")
        return (
            DimensionFilters.from_graphql(filters)
            .filter(survey.current_responses.all())
            .order_by("revision_created_at")
        )

    responses = graphene.List(
        graphene.NonNull(LimitedResponseType),
        filters=graphene.List(DimensionFilterInput),
        description=normalize_whitespace(resolve_responses.__doc__ or ""),
    )

    @staticmethod
    def resolve_response(survey: Survey, info, id: str):
        """
        Returns a single response to this survey regardless of language version used.
        Authorization required.
        """
        graphql_check_instance(survey, info, app=survey.app_name, field="responses")
        return survey.current_responses.filter(id=id).first()

    response = graphene.Field(
        FullResponseType,
        id=graphene.String(required=True),
    )

    @staticmethod
    def resolve_count_responses_by_current_user(survey: Survey, info):
        """
        Returns the number of responses to this survey by the current user.
        """
        if not info.context.user.is_authenticated:
            return 0

        return survey.current_responses.filter(revision_created_by=info.context.user).count()

    count_responses_by_current_user = graphene.Field(
        graphene.NonNull(graphene.Int),
        description=normalize_whitespace(resolve_count_responses_by_current_user.__doc__ or ""),
    )

    @staticmethod
    def resolve_count_responses(
        survey: Survey,
        info,
        filters: list[DimensionFilterInput] | None = None,
    ):
        """
        Returns the number of responses to this survey regardless of language version used.
        Authorization required.
        """
        graphql_check_instance(survey, info, app=survey.app_name, field="responses")
        return DimensionFilters.from_graphql(filters).filter(survey.current_responses.all()).count()

    count_responses = graphene.Field(
        graphene.NonNull(graphene.Int),
        filters=graphene.List(DimensionFilterInput),
        description=normalize_whitespace(resolve_count_responses.__doc__ or ""),
    )

    @staticmethod
    def resolve_summary(
        survey: Survey,
        info,
        lang: str = DEFAULT_LANGUAGE,
        filters: list[DimensionFilterInput] | None = None,
    ):
        """
        Returns a summary of responses to this survey.  If a language is specified,
        that language is used as the base for the combined fields. Order of fields
        not present in the base language is not guaranteed. Authorization required.
        """
        graphql_check_instance(survey, info, app=survey.app_name, field="responses")
        responses = (
            DimensionFilters.from_graphql(filters)
            .filter(survey.current_responses.all())
            .order_by("revision_created_at")
        )
        fields = survey.get_combined_fields(lang)
        valuesies = [response.get_processed_form_data(fields)[0] for response in responses.only("form_data")]
        summary = summarize_responses(fields, valuesies)

        return {slug: summary.model_dump(by_alias=True) for slug, summary in summary.items()}

    summary = graphene.Field(
        GenericScalar,
        lang=graphene.String(),
        filters=graphene.List(DimensionFilterInput),
        description=normalize_whitespace(resolve_summary.__doc__ or ""),
    )

    @staticmethod
    def resolve_dimensions(
        survey: Survey,
        info,
        # TODO unify naming
        is_list_filter: bool = False,
        is_shown_in_detail: bool = False,
        public_only: bool = True,
        key_dimensions_only: bool = False,
    ):
        """
        `is_list_filter` - only return dimensions that are shown in the list filter.
        `is_shown_in_detail` - only return dimensions that are shown in the detail view.
        If you supply both, you only get their intersection.
        """
        if public_only:
            dimensions = survey.universe.dimensions.filter(is_public=True)
        else:
            graphql_check_instance(
                survey,  # type: ignore
                info,
                field="dimensions",
                app=survey.app.value,
            )
            dimensions = survey.universe.dimensions.all()

        if is_list_filter:
            dimensions = dimensions.filter(is_list_filter=True)

        if is_shown_in_detail:
            dimensions = dimensions.filter(is_shown_in_detail=True)

        if key_dimensions_only:
            dimensions = dimensions.filter(is_key_dimension=True)

        return dimensions.order_by("order", "slug")

    dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(FullDimensionType)),
        is_list_filter=graphene.Boolean(),
        is_shown_in_detail=graphene.Boolean(),
        public_only=graphene.Boolean(),
        key_dimensions_only=graphene.Boolean(),
        description=normalize_whitespace(resolve_dimensions.__doc__ or ""),
    )

    @staticmethod
    def resolve_languages(parent: Survey, info):
        # TODO supported_languages order instead of alphabetical?
        return parent.languages.order_by("language")

    # TODO unify can_remove/can_delete naming across all apps
    @staticmethod
    def resolve_can_remove(survey: Survey, info):
        """
        Surveys that have language versions cannot be removed.
        Having language versions is also a prerequisite for a survey to have responses.
        """
        request: HttpRequest = info.context
        return survey.can_be_deleted_by(request)

    can_remove = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_can_remove.__doc__ or ""),
    )

    @staticmethod
    def resolve_can_remove_responses(survey: Survey, info):
        """
        Checks that the user has permission to remove responses to this survey.
        This requires proper CBAC permission and that `survey.protect_responses` is false.
        """
        request: HttpRequest = info.context
        return survey.can_responses_be_deleted_by(request)

    can_remove_responses = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_can_remove_responses.__doc__ or ""),
    )

    # TODO change to Scope
    event = graphene.NonNull(LimitedEventType)

    class Meta:
        model = Survey
        fields = (
            "slug",
            "active_from",
            "active_until",
            "responses_editable_until",
            "languages",
            "key_fields",
            "login_required",
            "anonymity",
            "max_responses_per_user",
            "protect_responses",
            "event",
            "cached_default_response_dimensions",
            "profile_field_selector",
            "registry",
        )
