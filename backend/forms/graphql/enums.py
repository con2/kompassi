import graphene

from ..models.enums import Anonymity, EditMode, SurveyPurpose

SurveyPurposeType = graphene.Enum.from_enum(SurveyPurpose)
AnonymiType = graphene.Enum.from_enum(Anonymity)
EditModeType = graphene.Enum.from_enum(EditMode)
