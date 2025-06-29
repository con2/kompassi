from __future__ import annotations

import graphene
import graphene_django

from forms.graphql.response_limited import LimitedResponseType
from graphql_api.language import DEFAULT_LANGUAGE
from involvement.models.involvement import Involvement
from program_v2.graphql.program_limited import LimitedProgramType

from .enums import InvolvementAppType, InvolvementTypeType


class LimitedInvolvementType(graphene_django.DjangoObjectType):
    """
    Represent Involvement (and the Person involved) without a way to traverse back to Person.
    """

    class Meta:
        model = Involvement
        fields = (
            "id",
            "is_active",
            "created_at",
            "updated_at",
            "program",
            "response",
            "type",
            "app",
        )

    program = graphene.Field(LimitedProgramType)
    response = graphene.Field(LimitedResponseType)
    program_offer = graphene.Field(LimitedResponseType)

    type = graphene.NonNull(InvolvementTypeType)
    app = graphene.NonNull(InvolvementAppType)

    @staticmethod
    def resolve_title(involvement: Involvement, info, lang: str = DEFAULT_LANGUAGE) -> str | None:
        return involvement.get_title(lang)

    title = graphene.String(lang=graphene.String())
    admin_link = graphene.String()
