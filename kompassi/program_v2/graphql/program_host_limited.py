from __future__ import annotations

import graphene
import graphene_django
from graphene.types.generic import GenericScalar

from kompassi.core.graphql.profile_limited import LimitedProfileType
from kompassi.involvement.graphql.enums import ProgramHostRoleType
from kompassi.involvement.models.involvement import Involvement


class LimitedProgramHostType(graphene_django.DjangoObjectType):
    class Meta:
        model = Involvement
        fields = (
            "id",
            "is_active",
            "created_at",
            "updated_at",
            "person",
            "cached_dimensions",
            "program_host_role",
        )

    person = graphene.NonNull(LimitedProfileType)
    cached_dimensions = graphene.NonNull(GenericScalar)
    program_host_role = graphene.Field(ProgramHostRoleType)
