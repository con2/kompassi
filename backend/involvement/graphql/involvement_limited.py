from __future__ import annotations

import graphene
import graphene_django

from core.graphql.profile_limited import LimitedProfileType
from involvement.models.involvement import Involvement
from program_v2.graphql.program_limited import LimitedProgramType


class LimitedInvolvementType(graphene_django.DjangoObjectType):
    """
    Represent Involvement (and the Person involved) without a way to traverse back to Event.
    """

    class Meta:
        model = Involvement
        fields = ("id", "is_active", "created_at", "updated_at", "person", "program")

    person = graphene.NonNull(LimitedProfileType)
    program = graphene.Field(LimitedProgramType)
