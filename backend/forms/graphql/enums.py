import graphene

from ..models.enums import Anonymity, SurveyApp, SurveyPurpose

SurveyAppType = graphene.Enum.from_enum(SurveyApp)
SurveyPurposeType = graphene.Enum.from_enum(SurveyPurpose)
AnonymiType = graphene.Enum.from_enum(Anonymity)
