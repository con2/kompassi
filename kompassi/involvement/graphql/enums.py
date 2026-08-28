import graphene

from ..models.enums import InvolvementType, NameDisplayStyle, ProgramHostRole

InvolvementTypeType = graphene.Enum.from_enum(InvolvementType)
NameDisplayStyleType = graphene.Enum.from_enum(NameDisplayStyle)
ProgramHostRoleType = graphene.Enum.from_enum(ProgramHostRole)
