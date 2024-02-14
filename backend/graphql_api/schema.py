from dataclasses import dataclass

import graphene
from django.conf import settings

from core.graphql.event import FullEventType
from core.graphql.profile import ProfileType
from core.models import Event, Person
from forms.graphql.mutations.create_survey import CreateSurvey
from forms.graphql.mutations.create_survey_response import CreateSurveyResponse
from forms.graphql.mutations.delete_survey_dimension import DeleteSurveyDimension
from forms.graphql.mutations.delete_survey_dimension_value import DeleteSurveyDimensionValue
from forms.graphql.mutations.init_file_upload import InitFileUpload
from forms.graphql.mutations.put_survey_dimension import PutSurveyDimension
from forms.graphql.mutations.put_survey_dimension_value import PutSurveyDimensionValue
from forms.graphql.mutations.update_response_dimensions import UpdateResponseDimensions
from forms.graphql.mutations.update_survey import UpdateSurvey


@dataclass
class Language:
    code: str
    name_fi: str
    name_en: str


LANGUAGES = [Language("fi", "suomi", "Finnish"), Language("en", "englanti", "English")]
DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


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


class Query(graphene.ObjectType):
    @staticmethod
    def resolve_event(root, info, slug: str):
        return Event.objects.filter(slug=slug).first()

    event = graphene.Field(FullEventType, slug=graphene.String(required=True))

    @staticmethod
    def resolve_profile(root, info):
        if not info.context.user.is_authenticated:
            return None

        try:
            return info.context.user.person
        except Person.DoesNotExist:
            return None

    profile = graphene.Field(ProfileType)


class Mutation(graphene.ObjectType):
    create_survey = CreateSurvey.Field()
    update_survey = UpdateSurvey.Field()

    create_survey_response = CreateSurveyResponse.Field()
    update_response_dimensions = UpdateResponseDimensions.Field()

    put_survey_dimension = PutSurveyDimension.Field()
    delete_survey_dimension = DeleteSurveyDimension.Field()

    put_survey_dimension_value = PutSurveyDimensionValue.Field()
    delete_survey_dimension_value = DeleteSurveyDimensionValue.Field()

    init_file_upload = InitFileUpload.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
