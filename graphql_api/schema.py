from dataclasses import dataclass

from django.conf import settings

import graphene
from graphene_django import DjangoObjectType

from core.models import Event
from forms.graphql import FormsEventMetaType, CreateEventSurveyResponse
from forms.models.meta import FormsEventMeta
from program_v2.graphql import ProgramV2EventMetaType


DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


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


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ("slug", "name")

    program = graphene.Field(ProgramV2EventMetaType)

    @staticmethod
    def resolve_program(parent: Event, info):
        return parent.program_v2_event_meta

    forms = graphene.Field(FormsEventMetaType)

    @staticmethod
    def resolve_forms(event: Event, info):
        return FormsEventMeta(event)


class Query(graphene.ObjectType):
    event = graphene.Field(EventType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_event(root, info, slug: str):
        return Event.objects.filter(slug=slug).first()


class Mutation(graphene.ObjectType):
    create_event_survey_response = CreateEventSurveyResponse.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
