from django.conf import settings

import graphene
from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar

from core.utils import get_ip, get_objects_within_period, normalize_whitespace
from access.cbac import graphql_query_cbac_required, graphql_check_access

from .models.form import EventForm
from .models.survey import EventSurvey
from .models.form_response import EventFormResponse
from .models.meta import FormsEventMeta

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class EventFormType(DjangoObjectType):
    fields = graphene.Field(
        GenericScalar,
        enrich=graphene.Boolean(
            description=(
                "Enriched fields have dynamic choices populated for them. This is the default. "
                'Pass enrich: false to get access to "raw" unenriched fields. This is used by the form editor.'
            ),
        ),
    )

    @staticmethod
    def resolve_fields(parent: EventForm, info, enrich: bool = True):
        if enrich:
            return parent.enriched_fields
        else:
            return parent.fields

    class Meta:
        model = EventForm
        fields = ("slug", "title", "description", "thank_you_message", "layout")


class EventFormResponseType(DjangoObjectType):
    values = graphene.Field(GenericScalar)

    @staticmethod
    def resolve_values(parent: EventFormResponse, info):
        return parent.values

    @staticmethod
    def resolve_language(parent: EventFormResponse, info):
        return parent.form.language

    language = graphene.Field(
        graphene.String,
        description="Language code of the form used to submit this response.",
    )

    class Meta:
        model = EventFormResponse
        fields = ("id", "form_data", "created_at")


class EventSurveyType(DjangoObjectType):
    title = graphene.Field(graphene.String, lang=graphene.String())

    @staticmethod
    def resolve_title(parent: EventSurvey, info, lang: str = DEFAULT_LANGUAGE):
        return form.title if (form := parent.get_form(lang)) else None

    is_active = graphene.Field(graphene.NonNull(graphene.Boolean))

    @staticmethod
    def resolve_is_active(parent: EventSurvey, info) -> bool:
        return parent.is_active

    form = graphene.Field(EventFormType, lang=graphene.String())

    @staticmethod
    def resolve_form(
        parent: EventSurvey,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ) -> EventForm | None:
        return parent.get_form(lang)

    @staticmethod
    def resolve_combined_fields(
        parent: EventSurvey,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ):
        """
        A survey's language versions may have differing fields. This field presents
        them combined as a single list of fields. If a language is specified,
        that language is used as the base for the combined fields. Order of fields
        not present in the base language is not guaranteed.
        """
        return [
            field.model_dump(
                exclude_none=True,
                by_alias=True,
            )
            for field in parent.get_combined_fields(lang)
        ]

    combined_fields = graphene.Field(
        GenericScalar,
        lang=graphene.String(),
        description=normalize_whitespace(resolve_combined_fields.__doc__ or ""),
    )

    @graphql_query_cbac_required
    @staticmethod
    def resolve_responses(survey: EventSurvey, info):
        """
        Returns the responses to this survey regardless of language version used.
        Authorization required.
        """
        return survey.responses.all()

    responses = graphene.List(
        graphene.NonNull(EventFormResponseType),
        description=normalize_whitespace(resolve_responses.__doc__ or ""),
    )

    class Meta:
        model = EventSurvey
        fields = (
            "slug",
            "active_from",
            "active_until",
        )


class EventSurveyResponseType(DjangoObjectType):
    class Meta:
        model = EventFormResponse
        fields = ("id", "form_data", "created_at")


class FormsEventMetaType(graphene.ObjectType):
    surveys = graphene.List(graphene.NonNull(EventSurveyType), include_inactive=graphene.Boolean())

    @staticmethod
    def resolve_surveys(meta: FormsEventMeta, info, include_inactive: bool = False):
        if include_inactive:
            graphql_check_access(meta, info, "surveys")
            qs = EventSurvey.objects.filter(event=meta.event)
        else:
            qs = get_objects_within_period(EventSurvey, event=meta.event)

        return qs

    survey = graphene.Field(EventSurveyType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_survey(meta: FormsEventMeta, info, slug: str):
        survey = EventSurvey.objects.get(event=meta.event, slug=slug)

        if not survey.is_active:
            graphql_check_access(meta, info, "survey")

        return survey


class CreateEventSurveyResponse(graphene.Mutation):
    class Arguments:
        event_slug = graphene.String(required=True)
        survey_slug = graphene.String(required=True)
        form_data = GenericScalar(required=True)
        locale = graphene.String()

    response = graphene.Field(EventSurveyResponseType)

    @staticmethod
    def mutate(
        root,
        info,
        event_slug: str,
        survey_slug: str,
        form_data: str,
        locale: str = "",
    ):
        survey = EventSurvey.objects.get(event__slug=event_slug, slug=survey_slug)

        if not survey.is_active:
            raise Exception("Survey is not active")

        form = survey.get_form(locale)

        ip_address = get_ip(info.context)
        created_by = user if (user := info.context.user) and user.is_authenticated else None

        response = EventFormResponse.objects.create(
            form=form,
            form_data=form_data,
            created_by=created_by,
            ip_address=ip_address,
        )

        return CreateEventSurveyResponse(response=response)  # type: ignore
