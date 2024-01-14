import graphene
from django.conf import settings
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from access.cbac import graphql_query_cbac_required
from core.utils import normalize_whitespace

from ..models.form import Form
from ..models.survey import Survey
from .form import FormType
from .form_response import FullResponseType, LimitedResponseType

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class SurveyType(DjangoObjectType):
    title = graphene.Field(graphene.String, lang=graphene.String())

    @staticmethod
    def resolve_title(parent: Survey, info, lang: str = DEFAULT_LANGUAGE):
        return form.title if (form := parent.get_form(lang)) else None

    is_active = graphene.Field(graphene.NonNull(graphene.Boolean))

    @staticmethod
    def resolve_is_active(parent: Survey, info) -> bool:
        return parent.is_active

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

    @graphql_query_cbac_required
    @staticmethod
    def resolve_responses(survey: Survey, info):
        """
        Returns the responses to this survey regardless of language version used.
        Authorization required.
        """
        return survey.responses.all()

    responses = graphene.List(
        graphene.NonNull(LimitedResponseType),
        description=normalize_whitespace(resolve_responses.__doc__ or ""),
    )

    @graphql_query_cbac_required
    @staticmethod
    def resolve_response(survey: Survey, info, id: str):
        """
        Returns a single response to this survey regardless of language version used.
        Authorization required.
        """
        return survey.responses.filter(id=id).first()

    response = graphene.Field(
        FullResponseType,
        id=graphene.String(required=True),
    )

    class Meta:
        model = Survey
        fields = (
            "slug",
            "active_from",
            "active_until",
            "languages",
            "key_fields",
        )
