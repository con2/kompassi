from __future__ import annotations

import graphene
import graphene_django
from graphene.types.generic import GenericScalar

from core.graphql.profile_limited import LimitedProfileType
from involvement.models.involvement import Involvement


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
        )

    person = graphene.NonNull(LimitedProfileType)
    cached_dimensions = graphene.NonNull(GenericScalar)
