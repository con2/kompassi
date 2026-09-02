import graphene

from ..models.enums import Anonymity, CanResponsesBeDeleted, EditMode, SurveyPurpose

SurveyPurposeType = graphene.Enum.from_enum(SurveyPurpose)
AnonymiType = graphene.Enum.from_enum(Anonymity)
EditModeType = graphene.Enum.from_enum(EditMode)
CanResponsesBeDeletedType = graphene.Enum.from_enum(CanResponsesBeDeleted)
