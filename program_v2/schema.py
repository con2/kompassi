from dataclasses import dataclass
from typing import Optional

from django.utils import translation

import graphene
from graphene_django import DjangoObjectType

from core.models import Event

from .models import Dimension, DimensionValue, ProgramDimensionValue, Program, ScheduleItem


DEFAULT_LANGUAGE = "fi"


def resolve_localized_field(parent, info, lang: Optional[str] = DEFAULT_LANGUAGE):
    """
    Given a LocalizedCharField or similar, this will resolve into its value in the currently active language.
    """
    with translation.override(lang):
        return getattr(parent, info.field_name).translate()


class DimensionType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field

    class Meta:
        model = Dimension
        fields = ("slug", "dimension_values")


class DimensionValueType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field

    class Meta:
        model = DimensionValue
        fields = ("slug", "dimension")


class ProgramDimensionValueType(DjangoObjectType):
    class Meta:
        model = ProgramDimensionValue
        fields = ("dimension", "dimension_value")


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
        fields = ("title", "slug", "program_dimension_values", "cached_dimensions", "schedule_items")


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
    def resolve_name(language: Language, info, lang: Optional[str] = DEFAULT_LANGUAGE):
        if lang == "fi":
            return language.name_fi
        else:
            return language.name_en


class DimensionFilterInput(graphene.InputObjectType):
    dimension = graphene.String()
    values = graphene.List(graphene.String)


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ("slug", "name")

    programs = graphene.List(
        ProgramType,
        filters=graphene.List(DimensionFilterInput),
    )

    @staticmethod
    def resolve_programs(
        event: Event,
        info,
        filters: Optional[list[DimensionFilterInput]] = None,
    ):
        queryset = Program.objects.filter(event=event)

        if filters:
            for filter in filters:
                queryset = queryset.filter(
                    program_dimension_values__dimension__slug=filter.dimension,
                    program_dimension_values__dimension_value__slug__in=filter.values,
                )

        return queryset

    dimensions = graphene.List(
        DimensionType,
    )

    @staticmethod
    def resolve_dimensions(
        event: Event,
        info,
    ):
        return Dimension.objects.filter(event=event)

    languages = graphene.List(
        LanguageType,
        event=graphene.String(required=True),
    )


class Query(graphene.ObjectType):
    event = graphene.Field(EventType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_event(root, info, slug: str):
        return Event.objects.filter(slug=slug).first()


schema = graphene.Schema(query=Query)
