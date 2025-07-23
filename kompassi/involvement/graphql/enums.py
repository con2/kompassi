import graphene

from ..models.enums import InvolvementApp, InvolvementType, NameDisplayStyle, ProgramHostRole

InvolvementAppType = graphene.Enum.from_enum(InvolvementApp)
InvolvementTypeType = graphene.Enum.from_enum(InvolvementType)
NameDisplayStyleType = graphene.Enum.from_enum(NameDisplayStyle)
ProgramHostRoleType = graphene.Enum.from_enum(ProgramHostRole)
