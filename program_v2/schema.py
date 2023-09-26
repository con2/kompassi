from dataclasses import dataclass
from typing import Optional

from django.utils import translation

import graphene
from graphene_django import DjangoObjectType

from .models import Dimension, DimensionValue, ProgramDimensionValue, Program, ScheduleItem


DEFAULT_LANGUAGE = "fi"


def resolve_localized_field(parent, info, **kwargs):
    """
    Given a LocalizedCharField or similar, this will resolve into its value in the currently active language.
    """
    return getattr(parent, info.field_name).translate()


class DimensionType(DjangoObjectType):
    title = graphene.String()
    resolve_title = resolve_localized_field

    class Meta:
        model = Dimension
        fields = ("slug", "dimension_values")


class DimensionValueType(DjangoObjectType):
    title = graphene.String()
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
    name: str


class LanguageType(graphene.ObjectType):
    code = graphene.String()
    name = graphene.String()


class DimensionFilterInput(graphene.InputObjectType):
    dimension = graphene.String()
    value = graphene.String()


class Query(graphene.ObjectType):
    languages_by_event = graphene.List(
        LanguageType,
        event=graphene.String(required=True),
        lang=graphene.String(),
    )
    dimensions_by_event = graphene.List(
        DimensionType,
        event=graphene.String(required=True),
        lang=graphene.String(),
    )
    programs_by_event = graphene.List(
        ProgramType,
        event=graphene.String(required=True),
        filters=graphene.List(DimensionFilterInput),
        lang=graphene.String(),
    )

    def resolve_languages_by_event(self, info, event, lang=None):
        # TODO hard-coded for now
        if lang == "fi":
            return [Language("fi", "suomi"), Language("en", "englanti")]
        else:
            return [Language("fi", "Finnish"), Language("en", "English")]

    def resolve_dimensions_by_event(
        self,
        info,
        event: str,
        lang: str = DEFAULT_LANGUAGE,
    ):
        translation.activate(lang)
        return Dimension.objects.filter(event__slug=event)

    def resolve_programs_by_event(
        self,
        info,
        event: str,
        filters: Optional[list[DimensionFilterInput]] = None,
        lang: str = DEFAULT_LANGUAGE,
    ):
        translation.activate(lang)
        queryset = Program.objects.filter(event__slug=event)

        if filters:
            for filter in filters:
                queryset = queryset.filter(
                    program_dimension_values__dimension__slug=filter.dimension,
                    program_dimension_values__dimension_value__slug=filter.value,
                )

        return queryset


schema = graphene.Schema(query=Query)
