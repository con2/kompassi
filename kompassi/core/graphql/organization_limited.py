import graphene
from graphene_django import DjangoObjectType

from kompassi.core.models.organization import Organization


class LimitedOrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = (
            "slug",
            "name",
        )

    timezone = graphene.NonNull(graphene.String)
