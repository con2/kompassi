import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from access.cbac import graphql_check_access
from core.utils import get_objects_within_period
from forms.graphql.form import FormType
from forms.models import Form
from graphql_api.utils import DEFAULT_LANGUAGE, resolve_localized_field

from .models import (
    Dimension,
    DimensionValue,
    OfferForm,
    Program,
    ProgramDimensionValue,
    ProgramV2EventMeta,
    ScheduleItem,
)


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
    class Meta:
        model = ScheduleItem
        fields = ("subtitle", "start_time")

    @staticmethod
    def resolve_length_minutes(parent: ScheduleItem, info):
        return parent.length.total_seconds() // 60

    length_minutes = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_end_time(parent: ScheduleItem, info):
        return parent.end_time

    end_time = graphene.NonNull(graphene.DateTime)

    @staticmethod
    def resolve_start_time_unix_seconds(parent: ScheduleItem, info):
        return int(parent.start_time.timestamp())

    start_time_unix_seconds = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_end_time_unix_seconds(parent: ScheduleItem, info):
        return int(parent.end_time.timestamp())

    end_time_unix_seconds = graphene.NonNull(graphene.Int)


class ProgramType(DjangoObjectType):
    cached_dimensions = graphene.Field(GenericScalar)

    class Meta:
        model = Program
        fields = ("title", "slug", "dimensions", "cached_dimensions", "schedule_items")


class DimensionFilterInput(graphene.InputObjectType):
    dimension = graphene.String()
    values = graphene.List(graphene.String)


class OfferFormType(DjangoObjectType):
    form = graphene.Field(FormType, lang=graphene.String())

    @staticmethod
    def resolve_form(
        parent: OfferForm,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ) -> Form | None:
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


class ProgramV2EventMetaType(DjangoObjectType):
    class Meta:
        model = ProgramV2EventMeta
        fields = ("skip_offer_form_selection",)

    programs = graphene.List(
        graphene.NonNull(ProgramType),
        filters=graphene.List(DimensionFilterInput),
    )

    @staticmethod
    def resolve_programs(
        meta: ProgramV2EventMeta,
        info,
        filters: list[DimensionFilterInput] | None = None,
    ):
        if filters is None:
            filters = []
        queryset = Program.objects.filter(event=meta.event)

        if filters:
            for filter in filters:
                queryset = queryset.filter(
                    dimensions__dimension__slug=filter.dimension,
                    dimensions__value__slug__in=filter.values,
                )

        return queryset

    dimensions = graphene.List(graphene.NonNull(DimensionType))

    @staticmethod
    def resolve_dimensions(meta: ProgramV2EventMeta, info):
        return Dimension.objects.filter(event=meta.event)

    offer_forms = graphene.List(graphene.NonNull(OfferFormType), include_inactive=graphene.Boolean())

    @staticmethod
    def resolve_offer_forms(meta: ProgramV2EventMeta, info, include_inactive: bool = False):
        if include_inactive:
            graphql_check_access(meta, info, "offer_forms")
            qs = OfferForm.objects.filter(event=meta.event)
        else:
            qs = get_objects_within_period(OfferForm, event=meta.event)

        return qs

    offer_form = graphene.Field(OfferFormType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_offer_form(meta: ProgramV2EventMeta, info, slug: str):
        return OfferForm.objects.get(event=meta.event, slug=slug)
