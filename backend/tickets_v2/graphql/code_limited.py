from enum import IntEnum

import graphene
from graphene_django import DjangoObjectType
from lippukala.models.code import Code


class CodeStatus(IntEnum):
    UNUSED = 0
    USED = 1
    MANUAL_INTERVENTION_REQUIRED = 2
    BEYOND_LOGIC = 3


class LimitedCodeType(DjangoObjectType):
    class Meta:
        model = Code
        fields = (
            "id",
            "code",
            "literate_code",
            "status",
            "used_on",
            "product_text",
        )

    @staticmethod
    def resolve_status(code: Code, info):
        return CodeStatus(code.status)

    status = graphene.NonNull(
        graphene.Enum.from_enum(CodeStatus),
        description="Status of the code. Kompassi uses the MIR state to indicate cancelled orders or otherwise revoked codes.",
    )
