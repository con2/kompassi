from dataclasses import dataclass

from django.utils import translation
from django.conf import settings

import graphene
from graphene_django import DjangoObjectType

from core.utils import get_objects_within_period
from core.models import Event
from forms.models import EventForm

from .models import Dimension, DimensionValue, ProgramDimensionValue, Program, ScheduleItem, OfferForm


DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


def resolve_localized_field(field_name: str):
    """
    Given a LocalizedCharField or similar, this will resolve into its value in the currently active language.
    Field name is required to be provided because info.field_name is in camelCase.
    """

    def _resolve(parent, info, lang: str = DEFAULT_LANGUAGE):
        with translation.override(lang):
            return getattr(parent, field_name).translate()

    return _resolve


class DimensionType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field("title")

    class Meta:
        model = Dimension
        fields = ("slug", "values")


class DimensionValueType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field("title")

    class Meta:
        model = DimensionValue
        fields = ("slug",)


class ProgramDimensionValueType(DjangoObjectType):
    class Meta:
        model = ProgramDimensionValue
        fields = ("dimension", "value")


class ScheduleItemType(DjangoObjectType):
    length_minutes = graphene.Int()
    end_time = graphene.DateTime()

    class Meta:
        model = ScheduleItem
        fields = ("subtitle", "start_time")

    @staticmethod
    def resolve_length_minutes(parent, info, **kwargs):
        return parent.length.total_seconds() // 60  # type: ignore

    @staticmethod
    def resolve_end_time(parent, info, **kwargs):
        return parent.end_time  # type: ignore


class ProgramType(DjangoObjectType):
    class Meta:
        model = Program
        fields = ("title", "slug", "dimensions", "cached_dimensions", "schedule_items")


@dataclass
class Language:
    code: str
    name_fi: str
    name_en: str


LANGUAGES = [Language("fi", "suomi", "Finnish"), Language("en", "englanti", "English")]


class LanguageType(graphene.ObjectType):
    code = graphene.String()
    name = graphene.String(lang=graphene.String())

    @staticmethod
    def resolve_name(
        language: Language,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ):
        if lang == "fi":
            return language.name_fi
        else:
            return language.name_en


class DimensionFilterInput(graphene.InputObjectType):
    dimension = graphene.String()
    values = graphene.List(graphene.String)


class EventFormType(DjangoObjectType):
    fields = graphene.Field(
        graphene.JSONString(),
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
        fields = ("slug", "title", "description", "active", "layout")


class OfferFormType(DjangoObjectType):
    form = graphene.Field(EventFormType, lang=graphene.String())

    @staticmethod
    def resolve_form(
        parent: OfferForm,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ) -> EventForm | None:
        return parent.get_form(lang)

    is_active = graphene.Field(graphene.NonNull(graphene.Boolean))

    @staticmethod
    def resolve_is_active(parent: OfferForm, info) -> bool:
        return parent.is_active

    short_description = graphene.String(lang=graphene.String())
    resolve_short_description = resolve_localized_field("short_description")

    class Meta:
        model = OfferForm
        fields = ("slug",)


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ("slug", "name")

    programs = graphene.List(
        graphene.NonNull(ProgramType),
        filters=graphene.List(DimensionFilterInput),
    )

    @staticmethod
    def resolve_programs(
        event: Event,
        info,
        filters: list[DimensionFilterInput] = [],
    ):
        queryset = Program.objects.filter(event=event)

        if filters:
            for filter in filters:
                queryset = queryset.filter(
                    dimensions__dimension__slug=filter.dimension,
                    dimensions__value__slug__in=filter.values,
                )

        return queryset

    dimensions = graphene.List(graphene.NonNull(DimensionType))

    @staticmethod
    def resolve_dimensions(event: Event, info):
        return Dimension.objects.filter(event=event)

    offer_forms = graphene.List(graphene.NonNull(OfferFormType), include_inactive=graphene.Boolean())

    @staticmethod
    def resolve_offer_forms(event: Event, info, include_inactive: bool = False):
        if include_inactive:
            # TODO must be admin
            qs = OfferForm.objects.filter(event=event)
        else:
            qs = get_objects_within_period(OfferForm, event=event)

        return qs

    offer_form = graphene.Field(OfferFormType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_offer_form(event: Event, info, slug: str):
        return OfferForm.objects.get(event=event, slug=slug)

    languages = graphene.List(graphene.NonNull(LanguageType))

    @staticmethod
    def resolve_languages(
        event: Event,
        info,
    ):
        # TODO
        return LANGUAGES

    # TODO program namespace that maps to ProgramV2EventMeta
    skip_offer_form_selection = graphene.Field(graphene.Boolean)

    @staticmethod
    def resolve_skip_offer_form_selection(
        event: Event,
        info,
    ):
        return meta.skip_offer_form_selection if (meta := event.program_v2_event_meta) else None


class Query(graphene.ObjectType):
    event = graphene.Field(EventType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_event(root, info, slug: str):
        return Event.objects.filter(slug=slug).first()


schema = graphene.Schema(query=Query)
