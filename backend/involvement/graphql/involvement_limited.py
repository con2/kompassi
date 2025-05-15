from __future__ import annotations

import graphene
import graphene_django

from core.graphql.person_limited import LimitedPersonType
from involvement.models.involvement import Involvement


class LimitedInvolvementType(graphene_django.DjangoObjectType):
    """
    Represent Involvement (and the Person involved) without a way to traverse back to Event.
    """

    class Meta:
        model = Involvement
        fields = ("id", "is_active", "created_at", "updated_at", "person")
        description = "Limited program host type. Used for the program host field in the program list."

    person = graphene.NonNull(LimitedPersonType)
