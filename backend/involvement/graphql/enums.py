import graphene

from ..models.enums import InvolvementApp, InvolvementType, NameDisplayStyle

InvolvementAppType = graphene.Enum.from_enum(InvolvementApp)
InvolvementTypeType = graphene.Enum.from_enum(InvolvementType)
NameDisplayStyleType = graphene.Enum.from_enum(NameDisplayStyle)
